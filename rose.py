# -*- coding: utf-8 -*-
# https://github.com/emilybache/GildedRose-Refactoring-Kata/tree/master/python

class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            if item.name != "Aged Brie" and item.name != "Backstage passes to a TAFKAL80ETC concert":
                if item.quality > 0:
                    if item.name != "Sulfuras, Hand of Ragnaros":
                        item.quality = item.quality - 1
            else:
                if item.quality < 50:
                    item.quality = item.quality + 1
                    if item.name == "Backstage passes to a TAFKAL80ETC concert":
                        if item.sell_in < 11:
                            if item.quality < 50:
                                item.quality = item.quality + 1
                        if item.sell_in < 6:
                            if item.quality < 50:
                                item.quality = item.quality + 1
            if item.name != "Sulfuras, Hand of Ragnaros":
                item.sell_in = item.sell_in - 1
            if item.sell_in < 0:
                if item.name != "Aged Brie":
                    if item.name != "Backstage passes to a TAFKAL80ETC concert":
                        if item.quality > 0:
                            if item.name != "Sulfuras, Hand of Ragnaros":
                                item.quality = item.quality - 1
                    else:
                        item.quality = item.quality - item.quality
                else:
                    if item.quality < 50:
                        item.quality = item.quality + 1


class Rose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            if item.name == "Aged Brie":
                item.quality = min([50, item.quality + 1])
            elif item.name == "Backstage passes to a TAFKAL80ETC concert":
                item.quality = min([50, item.quality + 1])
                item.quality = min([50, max([item.quality + _ for _ in [0, 1 if item.quality < 6 else 0, 2 if item.quality < 11 else 0]])])
            elif item.name == "Sulfuras, Hand of Ragnaros":
                pass
            else:
                item.quality = max([0, item.quality - 1])

            if item.name != "Sulfuras, Hand of Ragnaros":
                item.sell_in = item.sell_in - 1

            if item.sell_in < 0:
                if item.name == "Aged Brie":
                    item.quality = min([50, item.quality + 1])
                elif item.name == "Backstage passes to a TAFKAL80ETC concert":
                    item.quality = 0
                elif item.name == "Sulfuras, Hand of Ragnaros":
                    pass
                else:
                    item.quality = item.quality - 1


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


import unittest
import random
import copy

def judge_equal(items, gilded_rose, rose):
    error_count = 0
    for index in range(len(items)):
        item = items[index]
        o = gilded_rose.items[copy.deepcopy(index)]
        m = rose.items[copy.deepcopy(index)]
        if o.name == m.name and o.quality == m.quality and o.sell_in == m.sell_in:
            # print(item, "right")
            pass
        else:
            error_count += 1
            print(item, "error")
    return error_count

class GildedRoseTest(unittest.TestCase):
    def test_foo(self):
        sell_in = list(range(-10, 20))
        quality = list(range(-1, 50))
        names = ["Aged Brie", "Backstage passes to a TAFKAL80ETC concert", "Sulfuras, Hand of Ragnaros", "something else"]
        n = 100000
        c = 0
        error_count = 0
        while c > n:
            c += 1
            items = [Item(random.choice(names), random.choice(sell_in), random.choice(quality))]
            gilded_rose = GildedRose(copy.deepcopy(items))
            gilded_rose.update_quality()
            rose = Rose(copy.deepcopy(items))
            rose.update_quality()
            error_count_patch = judge_equal(items, gilded_rose, rose)
            error_count += error_count_patch
        print("all:%s, error:%s" % (n, error_count))



class GildedRoseTestV2(unittest.TestCase):
    items = [
             Item(name="+5 Dexterity Vest", sell_in=10, quality=20),
             Item(name="Aged Brie", sell_in=2, quality=0),
             Item(name="Elixir of the Mongoose", sell_in=5, quality=7),
             Item(name="Sulfuras, Hand of Ragnaros", sell_in=0, quality=80),
             Item(name="Sulfuras, Hand of Ragnaros", sell_in=-1, quality=80),
             Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=15, quality=20),
             Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=10, quality=49),
             Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=49),
             Item(name="Conjured Mana Cake", sell_in=3, quality=6),  # <-- :O
            ]
    error_count = 0
    days = 10
    for day in range(days):
        o = GildedRose(copy.deepcopy(items))
        o.update_quality()
        m = Rose(copy.deepcopy(items))
        m.update_quality()
        error_count_patch = judge_equal(items, o, m)
        error_count += error_count_patch
    print("error:%s" % (error_count,))

if __name__ == '__main__':
    unittest.main()
