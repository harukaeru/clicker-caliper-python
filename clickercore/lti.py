import json


class LtiUser:
    @classmethod
    def from_py_obj(cls, user_id, roles):
        ltiuser = LtiUser()
        ltiuser.id = user_id
        ltiuser.roles = roles
        return ltiuser

    def __init__(self):
        pass

    def has_role(self, role_name):
        return role_name in self.roles

    @classmethod
    def from_request(cls, request):
        ltiuser = LtiUser()
        ltiuser.id = request.POST['user_id']
        ltiuser.roles = []
        _roles = request.POST['roles']
        if _roles:
            for role_name in _roles.split(','):
                ltiuser.roles.append(role_name.strip())
        return ltiuser


def getParameter(name):
    return name

class LtiLaunch:
    def __init__(self):
        pass

    @classmethod
    def from_request(cls, request):
        ltilaunch = LtiLaunch()
        ltilaunch.user = LtiUser.from_request(request)
        ltilaunch.version = request.POST['lti_version']
        ltilaunch.messageType = request.POST["lti_message_type"]
        ltilaunch.resourceLinkId = request.POST["resource_link_id"]
        ltilaunch.contextId = request.POST["context_id"]
        ltilaunch.launchPresentationReturnUrl = request.POST["launch_presentation_return_url"]
        ltilaunch.toolConsumerInstanceGuid = request.POST["tool_consumer_instance_guid"]
        return ltilaunch

    def getUser(self):
        return self.user

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

    @classmethod
    def from_json(cls, data):
        json_data = json.loads(data)
        ltilaunch = LtiLaunch()
        for k, v in json_data.items():
            if k == 'user':
                ltilaunch.user = LtiUser.from_py_obj(v['id'], v['roles'])
                print('l', ltilaunch.user)
            else:
                setattr(ltilaunch, k, v)
        return ltilaunch
