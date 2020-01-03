
class ContentBaseQueryset:
    def get_queryset(self):
        teacher = self.request.user.teacher
        contents = teacher.contents.all()
        return contents
