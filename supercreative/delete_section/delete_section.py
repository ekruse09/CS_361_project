from supercreative.models import Section, UserCourseAssignment
from django.core.exceptions import ObjectDoesNotExist

def delete_section(delsection):
    if not delsection:
        return "No Section detected"
    try:
        section = Section.objects.get(section_id=delsection)
    except ObjectDoesNotExist:
        return "Section does not exist"
    UserCourseAssignment.objects.filter(section_id=section).delete()
    section.delete()
    return "Section deletion was successful"
