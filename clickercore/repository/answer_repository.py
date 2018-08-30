from clickercore.models import Answer


class AnswerRepository:
    @staticmethod
    def findByUserIdAndClickerItem(userId, clickerItem):
        return Answer.objects.filter(userId=userId, clickerItem=clickerItem)

    @staticmethod
    def save(answer):
        answer.save()
