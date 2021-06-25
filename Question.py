class Question:
    count_id = 0

    def __init__(self, name, email, feedback, remark):
        Question.count_id += 1
        self.__question_id = Question.count_id
        self.__name = name
        self.__email = email
        self.__feedback = feedback
        self.__remark = remark

    def get_question_id(self):
        return self.__question_id

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_feedback(self):
        return self.__feedback

    def get_remark(self):
        return self.__remark

    def set_name(self, name):
        self.__name = name

    def set_email(self, email):
        self.__email = email

    def set_feedback(self, feedback):
        self.__feedback = feedback

    def set_remark(self, remark):
        self.__remark = remark