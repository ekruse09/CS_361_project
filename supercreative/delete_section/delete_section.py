from supercreative.models import Section, UserCourseAssignment
def delete_section(user, delsection):
    if user in ["administrator"]
    if not Section.objects.filter(delsection.section).exists():
        return False
    UserCourseAssignment.objects.filter(delsection.section).delete()
    Section.objects.get(section_id=delsection).delete()
    return True