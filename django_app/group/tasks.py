from config.celery import app


@app.task
def task_update_num_of_member(group_pk):
    from group.models import MyGroup
    group = MyGroup.objects.get(pk=group_pk)
    group.calc_num_of_members()
    return group.num_of_members
