import os
import numpy as np


class posture(object):
    def __init__(self, diaperworkarea=None, personworkarea=None, filterarea=None):
        self.diaperworkarea = diaperworkarea
        self.personworkarea = personworkarea
        self.filterarea = filterarea

    def getpost(self, activethings):
        if self.filterarea is not None:
            activethings = [thing for thing in activethings if thingisinarea(self.filterarea, thing['xyxy'])]

        persons = [thing for thing in activethings if thing['label'] == 'person']
        diapers = [thing for thing in activethings if thing['label'] == 'diaper']
        persons_butt = get_zoomobj(persons, scale=0.5)

        if self.personworkarea is not None:
            inworkareapersons = [thing for thing in persons if thingisinarea(self.personworkarea, thing['xyxy'])]
            inpersonworkareadiapers = [thing for thing in diapers if thingisinarea(self.personworkarea, thing['xyxy'])]
            notinworkareapersons = [thing for thing in persons if not thingisinarea(self.personworkarea, thing['xyxy'])]
        else:
            inworkareapersons, notinworkareapersons = get_Intersectionobj(persons, persons)
            if len(persons)==1:
                notinworkareapersons = []
            inpersonworkareadiapers = []

        if self.diaperworkarea is not None:
            inworkareadiapers = [thing for thing in diapers if thingisinarea(self.diaperworkarea, thing['xyxy'])]
            notinworkareadiapers = [thing for thing in diapers if not thingisinarea(self.diaperworkarea, thing['xyxy'])]
        else:
            inworkareadiapers, notinworkareadiapers = get_Intersectionobj(diapers, persons_butt,method='boxandpoint')

        post = {}
        post['count_person'] = len(persons)
        post['count_diaper'] = len(diapers)
        post['count_inworkareaperson'] = len(inworkareapersons)
        post['count_inworkareadiaper'] = len(inworkareadiapers)
        post['count_inpersonworkareadiapers'] = len(inpersonworkareadiapers)
        post['count_notinworkareaperson'] = len(notinworkareapersons)
        post['count_notinworkareadiaper'] = len(notinworkareadiapers)
        if self.diaperworkarea is not None:
            post['count_persontouchdiapernotinworkarea'] = getcount_persontouchobj(notinworkareapersons,
                                                                                   notinworkareadiapers)
            post['count_persontouchdiaperininworkarea'] = getcount_persontouchobj(inworkareapersons,
                                                                                  inworkareadiapers)
        else :
            post['count_persontouchdiapernotinworkarea'] = getcount_persontouchobj(notinworkareapersons,
                                                                                   diapers)
            post['count_persontouchdiaperininworkarea'] = getcount_persontouchobj(inworkareapersons,
                                                                                  diapers)
        return post


def get_zoomobj(objs, scale=0.5):
    zoomobjs = []
    for obj in objs:
        zoomobj = obj.copy()
        zoomobj['xyxy'] = xyxy2zoomxyxy(zoomobj['xyxy'], scale=scale)
        zoomobjs.append(zoomobj)
    return objs


def get_Intersectionobj(objs_A, objs_B, method='iou'):
    inworkareapersons = []
    notinworkareapersons = []
    AequalB = objs_A==objs_B
    for i, obj_a in enumerate(objs_A):
        iinothers = 0
        for j, obj_b in enumerate(objs_B):
            intersection_bool = get_iou(obj_b['xyxy'], obj_a['xyxy']) != 0 if method == 'iou' else thingisinarea(obj_b['xyxy'], obj_a['xyxy'])
            if AequalB:
                if i != j and intersection_bool:
                    iinothers += 1
            else:
                if intersection_bool:
                    iinothers += 1
        if iinothers > 0:
            inworkareapersons.append(obj_a)
        else:
            notinworkareapersons.append(obj_a)
    return inworkareapersons, notinworkareapersons


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
            # print('avex','avey',avex,avey)
            # print('person_xyxy',person_xyxy)
            # print('checkpointisinbox(person_xyxy, avex, avey)',checkpointisinbox(person_xyxy, avex, avey))
            if checkpointisinbox(person_xyxy, avex, avey):
                count_persontouchobj += 1
    return count_persontouchobj


def checkpointisinbox(workarea, point_x, point_y):
    return True if point_x > workarea[0] and point_x < workarea[2] and point_y > workarea[1] and point_y < \
                   workarea[3] else False


def xyxy2avexy(xyxy):
    avex = (xyxy[0] + xyxy[2]) / 2
    avey = (xyxy[1] + xyxy[3]) / 2
    return avex, avey


def xyxy2zoomxyxy(xyxy, scale=1.0):
    w = xyxy[2] - xyxy[0]
    h = xyxy[3] - xyxy[1]
    zoomw = w * scale
    zoomh = h * scale
    avex, avey = xyxy2avexy(xyxy)
    zoomxyxy = np.array([avex - 0.5 * zoomw, avey - 0.5 * zoomh, avex + 0.5 * zoomw, avey + 0.5 * zoomh]).astype('int')
    return zoomxyxy


def get_iou(boxA, boxB):
    boxA = [int(x) for x in boxA]
    boxB = [int(x) for x in boxB]

    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)

    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)

    iou = interArea / float(boxAArea + boxBArea - interArea)
    return iou


class action(object):
    def __init__(self, window, threscount):
        self.window = window
        self.threscount = threscount

    def takediapernotinarea(self, postdf, threscount=1):
        col = 'count_persontouchdiapernotinworkarea'
        windowpostdf = postdf[-self.window['takediapernotinarea']:]
        count = (windowpostdf[col] >= threscount).sum()
        return count >= self.threscount['takediapernotinarea']

    def personinarea(self, postdf, threscount=1):
        col = 'count_inworkareaperson'
        windowpostdf = postdf[-self.window['personinarea']:]
        count = (windowpostdf[col] >= threscount).sum()
        return count >= self.threscount['personinarea']

    def diaperinarea(self, postdf, threscount=1):
        col = 'count_inworkareadiaper'
        windowpostdf = postdf[-self.window['diaperinarea']:]
        count = (windowpostdf[col] >= threscount).sum()
        return count >= self.threscount['diaperinarea']

    def diaperinpersonarea(self, postdf, threscount=1):
        col = 'count_inpersonworkareadiapers'
        windowpostdf = postdf[-self.window['diaperinarea']:]
        count = (windowpostdf[col] >= threscount).sum()
        return count >= self.threscount['diaperinarea']

    def getaction(self, postdf):
        action_takediapernotinarea = self.takediapernotinarea(postdf)
        action_onepersoninarea = self.personinarea(postdf, threscount=1)
        action_twopersoninarea = self.personinarea(postdf, threscount=2)
        action_diaperinarea = self.diaperinarea(postdf)
        action_diaperinpersonarea = self.diaperinpersonarea(postdf)
        return {'action_takediapernotinarea': action_takediapernotinarea,
                'action_onepersoninarea': action_onepersoninarea,
                'action_twopersoninarea': action_twopersoninarea,
                'action_diaperinarea': action_diaperinarea,
                'action_diaperinpersonarea': action_diaperinpersonarea}


class comboaction(object):
    def __init__(self, patient):
        self.status = 'waittrigger'
        self.patient = patient
        self.count = 0

    def update(self, action):
        # original_status = self.status
        if self.status == 'waittrigger':
            if action['action_takediapernotinarea']:
                self.status = 'takediapernotinarea'
                self.count = 0
            else:
                self.count += 1
        elif self.status == 'takediapernotinarea':
            if action['action_twopersoninarea']:
                self.status = 'twopersoninarea'
                self.count = 0
            else:
                self.count += 1
        elif self.status == 'twopersoninarea':
            if action['action_diaperinarea']:
                self.status = 'replacediaper'
                self.count = 0
            else:
                self.count += 1
        elif self.status == 'replacediaper':
            # if action['action_takediapernotinarea'] or (
            #         not action['action_diaperinarea'] and not action['action_twopersoninarea']):
            #     self.status = 'finish'
            #     self.count = 0
            if not action['action_diaperinarea'] and not action['action_twopersoninarea']:
                self.status = 'finish'
                self.count = 0
            else:
                self.count += 1
        else:
            self.status = 'waittrigger'
            self.count = 0

        if self.count >= self.patient:
            self.status = 'waittrigger'
            self.count = 0

        return self.status,self.count


class timer(object):
    pass


class counter(object):
    pass
