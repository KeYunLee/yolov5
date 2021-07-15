import os


class posture(object):
    def __init__(self, diaperworkarea, personworkarea, filterarea = None):
        self.diaperworkarea = diaperworkarea
        self.personworkarea = personworkarea
        self.filterarea = filterarea

    def getpost(self, activethings):
        if self.filterarea is not None:
            activethings = [thing for thing in activethings if thingisinarea(self.filterarea,thing['xyxy']) ]
        post = {}
        persons = [thing for thing in activethings if thing['label'] == 'person']
        diapers = [thing for thing in activethings if thing['label'] == 'diaper']
        inworkareapersons = [thing for thing in activethings if
                             thing['label'] == 'person' and thingisinarea(self.personworkarea, thing['xyxy'])]
        inworkareadiapers = [thing for thing in activethings if
                             thing['label'] == 'diaper' and thingisinarea(self.diaperworkarea, thing['xyxy'])]
        notinworkareapersons = [thing for thing in activethings if
                                thing['label'] == 'person' and not thingisinarea(self.personworkarea, thing['xyxy'])]
        notinworkareadiapers = [thing for thing in activethings if
                                thing['label'] == 'diaper' and not thingisinarea(self.diaperworkarea, thing['xyxy'])]

        post['count_person'] = len(persons)
        post['count_diaper'] = len(diapers)
        post['count_inworkareaperson'] = len(inworkareapersons)
        post['count_inworkareadiaper'] = len(inworkareadiapers)
        post['count_notinworkareaperson'] = len(notinworkareapersons)
        post['count_notinworkareadiaper'] = len(notinworkareadiapers)
        post['count_persontouchdiapernotinworkarea'] = getcount_persontouchobj(notinworkareapersons,
                                                                               notinworkareadiapers)
        post['count_persontouchdiaperininworkarea'] = getcount_persontouchobj(inworkareapersons,
                                                                              inworkareadiapers)
        return post

def thingisinarea(area, thing_xyxy):
    avex, avey = xyxy2avexy(thing_xyxy)
    isinworkarea = checkpointisinbox(area, avex, avey)
    return isinworkarea


def getcount_persontouchobj(persons, objs):
    count_persontouchobj = 0
    for person in persons:
        person_xyxy = person['xyxy']
        for obj in objs:
            diaper_xyxy = obj['xyxy']
            avex, avey = xyxy2avexy(diaper_xyxy)
            if checkpointisinbox(person_xyxy, avex, avey):
                count_persontouchobj += 1
    return count_persontouchobj


def checkpointisinbox(workarea, point_x, point_y):
    return True if point_x > workarea[0] and point_x < workarea[2] and point_y > workarea[1] and point_y < \
                   workarea[3] else False


def xyxy2avexy(thing_xyxy):
    avex = (thing_xyxy[0] + thing_xyxy[2]) / 2
    avey = (thing_xyxy[1] + thing_xyxy[3]) / 2
    return avex, avey


class comboaction(object):
    pass


class timer(object):
    pass


class counter(object):
    pass
