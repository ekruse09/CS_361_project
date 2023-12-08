from supercreative.models import Section, UserCourseAssignment


def delete_section(delsection):
    if not Section.objects.filter(delsection.section).exists():
        return "Section does not exist"
    if delsection in "":
        return "No Section detected"
    UserCourseAssignment.objects.filter(delsection.section).delete()
    Section.objects.get(section_id=delsection).delete()
    return "Section deletion was successful"
