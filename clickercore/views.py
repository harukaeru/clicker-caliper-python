import uuid
import datetime
import logging
from django.template import Template, Context
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponse
from clickercore.caliper_session import CaliperSession
from clickercore.lti import LtiLaunch
from clickercore.models import ClickerItem, ClickerOption, Answer
from clickercore.services.answer_service import AnswerService
from clickercore.services.clicker_item_service import ClickerItemService
from clickercore.services.mock_key_service import MockKeyService

def get_now():
    n = datetime.datetime.now().isoformat()
    print('n', n)
    return n

def get_ltilaunch(request):
    ltilaunch = request.session['ltiLaunch']
    ltilaunch = LtiLaunch.from_json(ltilaunch)
    return ltilaunch


def render_modellike(template_path, *, modellike):
    f = open('clickercore/templates/' + template_path).read()
    t = Template(f)
    if modellike is None:
        context = {}
    else:
        context = modellike.context
    html = t.render(Context(context))
    return HttpResponse(html)

class TempModel:
    def __init__(self):
        self.context = {}

    def addAttribute(self, attr, value):
        self.context[attr] = value

    def show(self):
        print(self.context)


@csrf_exempt
def index(request):
    model = TempModel()

    if request.method == 'GET':
        ltilaunch = get_ltilaunch(request)
        resourceLinkId = ltilaunch.resourceLinkId

        # Check user's role
        print('user', ltilaunch.user)
        isInstructor = ltilaunch.user.has_role("Instructor")
        model.addAttribute("isInstructor", isInstructor);

        # Get active items
        activeClickerItemList = ClickerItemService.findByResourceLinkIdAndStatus(
            resourceLinkId, ClickerItem.STATUS_ONGOING
        )
        if len(activeClickerItemList) > 0:
            # If active items exists
            activeClickerItem = activeClickerItemList[0]
            model.addAttribute("activeClickerItem", activeClickerItem);

            answer = AnswerService.findByUserIdAndClickerItem(
                ltilaunch.user.id, activeClickerItem
            )
            model.addAttribute("answer", answer);

        # Get all items
        clickerItemList = ClickerItemService.findByResourceLinkId(resourceLinkId);
        model.addAttribute("clickerItemList", clickerItemList);

        model.show()

        return render_modellike('index.html', modellike=model)

@csrf_exempt
def new(request):
    # GET /new
    return render_modellike('new.html', modellike=None)


@csrf_exempt
def clicker_create(request):
    # POST /clicker/create
    ltilaunch = get_ltilaunch(request)

    clickerItem = ClickerItem()
    clickerItem.resourceLinkId = ltilaunch.resourceLinkId   # LTI 経由で起動したコースのリソースIDを取得
    clickerItem.body = request.POST['body']
    clickerItem.status = ClickerItem.STATUS_NEW
    ClickerItemService.save(clickerItem)

    for i in [0, 1]:
        title = request.POST['clickerOptions[' + str(i) + '].title']
        option = ClickerOption(clickerItem=clickerItem, title=title)
        option.save()

    return redirect('main-view')



# GET /clicker/{clickerItemId}
# 設問の個別画面
# @GetMapping(value = "{clickerItemId}")
@csrf_exempt
def clicker_show(request, **kwargs):
    clickerItemId = kwargs.get('clickerItemId')
    clickerItem = ClickerItemService.findById(clickerItemId)
    model = TempModel()
    model.addAttribute("clickerItem", clickerItem);

    return render_modellike('show.html', modellike=model)

# POST /clicker/{clickerItemId}/answer
# 回答処理
@csrf_exempt
def clicker_answer(request, **kwargs):
    # Get launch params
    ltilaunch = get_ltilaunch(request)
    answer = Answer(userId=ltilaunch.user.id)
    answer.user = ltilaunch.user
    if request.POST.get('clickerOption.id'):
        answer.clickerOption = ClickerOption.objects.get(id=request.POST.get('clickerOption.id'))
    else:
        return redirect('main-view')

    clickerItemId = kwargs.get('clickerItemId')
    clickerItem = ClickerItemService.findById(clickerItemId)
    if request.POST.get('body'):
        clickerItem.body = request.POST.get('body')

    answer.clickerItem = clickerItem

    AnswerService.save(answer);

    return redirect('main-view')

# POST /clicker/{clickerItemId}/start
# 開始処理
# @PostMapping(value = "{clickerItemId}/start")
@csrf_exempt
def clicker_start(request, **kwargs):
# public String start(@PathVariable("clickerItemId") final Long clickerItemId){
    # Set status ONGOING (enabled)

    clickerItemId = kwargs.get('clickerItemId')
    clickerItem = ClickerItemService.findById(clickerItemId)
    ClickerItemService.updateStatus(clickerItemId, ClickerItem.STATUS_ONGOING)

    return redirect('main-view')

# POST /clicker/{clickerItemId}/stop
# 終了処理
# @PostMapping(value = "{clickerItemId}/stop")
# public String stop(@PathVariable("clickerItemId") final Long clickerItemId){
@csrf_exempt
def clicker_stop(request, **kwargs):
    # Set status COMPLETED (disabled)
    # ClickerItemService.updateStatus(clickerItemId, ClickerItem.Status.COMPLETED);
    clickerItemId = kwargs.get('clickerItemId')
    clickerItem = ClickerItemService.findById(clickerItemId)
    ClickerItemService.updateStatus(clickerItemId, ClickerItem.STATUS_COMPLETED)

    return redirect('main-view')


@csrf_exempt
def launch(request):
    print('POST', request.POST)
    # POST /launch
    # LTI で LMS から起動する際のエンドポイント

    # Set session value
    # LMS から遷移したときしかパラメータは取得できないためセッションに格納して利用
    launch = LtiLaunch.from_request(request)
    # launch = result.getLtiLaunchResult()
    # print('request.session', request.session)
    # print('dir(request.session)', dir(request.session))
    print('requests.session', request.session)
    request.session['ltiLaunch'] = launch.to_json()
    print('ltilaunch', request.session['ltiLaunch'])
    # request.session.setAttribute('ltilaunch', launch)
        # final LtiLaunch launch = result.getLtiLaunchResult();   // LTI におけるパラメータを LtiLaunch オブジェクトとして取得
        # session.setAttribute("ltiLaunch", launch);  // そのままセッションに格納

    # Logging with Caliper
    # Get current DateTime
    now = datetime.datetime.now()
    if CaliperSession().sendSessionLoggedIn(launch.user, uuid.uuid4().hex, get_now()):
        # イベント送信成功
        logging.info("SessionEvent(Logged In) was sent successfully.")
    else:
        # イベント送信失敗
        logging.error("Failed to send SessionEvent(Logged In).")

    return redirect('main-view')
