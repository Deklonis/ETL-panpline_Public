import re
from components.sklonenie import morph_analize
from components.fromactdb import first_word_post
import pandas as pd



def all_first_word_func():
    all_post_w_slon = ["генеральный", "директор", "начальник", "заместитель", "главный", "ведущий", "старший", "менеджер", "руководитель", "инженер", "технолог", "механик", "конструктор", "геолог", "химик", "эксперт", "специалист", "оператор", "мастер", "бригадир", "аналитик", "маркетолог", "программист", "преподаватель", "доцент", "профессор", "аспирант", "лаборант", "заведующий", "управляющий", "советник", "координатор", "администратор", "консультант", "ассистент", "департамент"]
    all_post = []
    for i in all_post_w_slon+first_word_post():
        all_post.extend(morph_analize(i))
    all_post = sorted(list(set(all_post)))
    return all_post
