
class LocationBaseQueryset:
    def get_queryset(self):
        teacher = self.request.user.teacher
        locations = teacher.locations.all()
        return locations
