import caliper


class CaliperSession:
    ENDPOINT =  "http://c19.media.hosei.ac.jp/lrs/ims201805s/"
    API_KEY = "Basic dXNlcjE6eHdYRnRqWnY="
    SENSOR_ID = "sensorId";
    CLIENT_ID = "clientId";
    APP_ID = "http://localhost:8080";
    APP_NAME = "Clicker Java";

    def __init__(self):
        self.sensor = caliper.Sensor(self.SENSOR_ID)
        self.options = caliper.base.HttpOptions(
            api_key=self.API_KEY, host=self.ENDPOINT
        )
        client = caliper.sensor.Client(self.options)
        self.sensor.register_client(
            self.CLIENT_ID, client
        )

        self.app = caliper.entities.SoftwareApplication(
            id=self.APP_ID, name=self.APP_NAME
        )

    def sendSessionLoggedIn(self, user, session_id, loginTime):

        actor = (
            caliper.entities.Person(name=user.id, id="/users/" + str(user.id))
        )

        session = caliper.entities.Session(
            id=self.APP_ID + "/sessions/" + session_id,
            user=actor,
            dateCreated=loginTime,
            dateModified=loginTime,
            startedAtTime=loginTime,
        )

        location = caliper.entities.MediaLocation(
            id=self.APP_ID + "/launch",
            name="Launch Page",
        )

        print('loginTime', loginTime)
        # Caliper に送信するイベントオブジェクトを作成
        sessionEvent = caliper.events.SessionEvent(
            actor=actor,
            action=caliper.events.SESSION_EVENT_ACTIONS['LOGGED_IN'],
            object=self.app,
            generated=session,
            target=location,
            eventTime=loginTime,
        )

        try:
            self.sensor.send(event=sessionEvent)
            return True;
        except Exception as e:
            print(e)
            raise Exception('おくれてない')
            return False
