from clickercore.models import ClickerItem


class ClickerItemRepository:
    @staticmethod
    def findById(id):
        return ClickerItem.objects.get(id=id)

    @staticmethod
    def findByResourceLinkId(resourceLinkId):
        return ClickerItem.objects.filter(resourceLinkId=resourceLinkId)

    @staticmethod
    def findByResourceLinkIdAndStatus(resourceLinkId, status):
        return ClickerItem.objects.filter(resourceLinkId=resourceLinkId, status=status)

    @staticmethod
    def save(clickerItem):
        clickerItem.save()
