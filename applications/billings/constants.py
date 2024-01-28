class CategoryChoices:
    COFFEE = 1
    BEVERAGE = 2
    TEA = 3
    SMOOTHIE = 4
    DESSERT = 5
    BAKERY = 6
    OTHER = 7

    CHOICES = [
        (COFFEE, '커피'),
        (BEVERAGE, '음료'),
        (TEA, '티'),
        (SMOOTHIE, '스무디'),
        (DESSERT, '디저트'),
        (BAKERY, '베이커리'),
        (OTHER, '기타'),
    ]

    CATEGORY_IN_DB = {
        "커피": COFFEE,
        "음료": BEVERAGE,
        "티": TEA,
        "스무디": SMOOTHIE,
        "디저트": DESSERT,
        "베이커리": BAKERY,
        "기타": OTHER,
    }


class SizeChoices:
    SMALL = 1
    LARGE = 2
    ETC = 3

    CHOICES = [
        (SMALL, 'small'),
        (LARGE, 'large'),
        (ETC, 'etc'),
    ]

    SIZE_IN_DB = {
        "small": SMALL,
        "large": LARGE,
        "etc": ETC,
    }

