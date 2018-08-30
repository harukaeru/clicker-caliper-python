from clickercore.repository.answer_repository import AnswerRepository
from clickercore.repository.clicker_item_repository import ClickerItemRepository


class AnswerService:
    @staticmethod
    def findByUserIdAndClickerItem(userId, clickerItem):
        return AnswerRepository.findByUserIdAndClickerItem(userId, clickerItem);

    @staticmethod
    def save(answer):
        savedAnswer = AnswerRepository.findByUserIdAndClickerItem(
            answer.user.id, answer.clickerItem
        )
        # if savedAnswer:
        #     # Update if already answered
        #     answer.id = savedAnswer.id

        return AnswerRepository.save(answer)
