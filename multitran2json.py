import sqlite3
from constants import *

# [
#   {
#       "language": {"lang1": "lang2"},
#       "groups": [
#       {
#           "name": "group name",
#           "words": {
#               "word1":["translation1", "translation2"],
#               "word2":["translation"]
#           }
#       },
#       {
#           "name": "group name",
#           ...
#       }
#   }
# ]


def convert(file: str):
    def getData(sql):
        cursor.execute(sql)
        return cursor.fetchall()

    def getLanguageObjectIndex(lang1: str, lang2: str):
        for x in range(0, len(dictionary)):
            if dictionary[x][JSONKeys.LANGUAGE] == {lang1: lang2}:
                return x

    def getGroupObjectIndex(name: str, langIndex: int):
        langGroups = dictionary[langIndex][JSONKeys.GROUPS]
        for x in range(0, len(langGroups)):
            if langGroups[x][JSONKeys.GROUP_NAME] == name:
                return x

    dictionary = []

    conn = sqlite3.connect(file)
    cursor = conn.cursor()

    translationTable = getData("SELECT * FROM word_translation")

    def sqlGetById(table: str, id: int):
        return getData("SELECT * FROM " + table + " WHERE id=" + str(id))[0]

    for x in translationTable:
        wordData = sqlGetById("word", x[Translation.WORD_ID])
        translationData = sqlGetById("word", x[Translation.TRANSLATION_ID])
        groupData = sqlGetById("favorite", wordData[Word.GROUP_ID])
        word = wordData[Word.WORD]
        translation = translationData[Word.WORD]
        wordLang = wordData[Word.LANGUAGE]
        translationLang = translationData[Word.LANGUAGE]

        index = getLanguageObjectIndex(wordLang, translationLang)

        if index is None:
            index = len(dictionary)
            dictionary.append({
                JSONKeys.LANGUAGE: {wordLang: translationLang},
                JSONKeys.GROUPS: []
            })

        groupIndex = getGroupObjectIndex(groupData[Group.NAME], index)

        if groupIndex is None:
            groupIndex = len(dictionary[index][JSONKeys.GROUPS])
            dictionary[index][JSONKeys.GROUPS].append({
                JSONKeys.GROUP_NAME: groupData[Group.NAME],
                JSONKeys.WORDS: {}
            })

        groupWords = dictionary[index][JSONKeys.GROUPS][groupIndex][JSONKeys.WORDS]
        if word in groupWords:
            groupWords[word].append(translation)
        else:
            groupWords[word] = [translation]

    return dictionary
