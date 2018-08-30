from clickercore.repository.clicker_item_repository import ClickerItemRepository


class ClickerItemService:
    @staticmethod
    def findById(id):
        return ClickerItemRepository.findById(id)

    @staticmethod
    def findByResourceLinkId(resourceLinkId):
        return ClickerItemRepository.findByResourceLinkId(resourceLinkId)

    @staticmethod
    def findByResourceLinkIdAndStatus(resourceLinkId, status):
        return ClickerItemRepository.findByResourceLinkIdAndStatus(resourceLinkId, status)

    @staticmethod
    def save(clickerItem):
        return ClickerItemRepository.save(clickerItem)

    @staticmethod
    def updateStatus(id, status):
        clickerItem = ClickerItemRepository.findById(id)
        clickerItem.status = status
        ClickerItemRepository.save(clickerItem)

        return clickerItem
