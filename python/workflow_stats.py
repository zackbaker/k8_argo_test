import argparse
import datetime as dt

import pytz
import json


def run():
    args = set_arguments()

    workflow_name = get_name(args.workflow_name)

    end_time = dt.datetime.strptime(dt.datetime.now(pytz.utc).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
    creation_time = get_creation_time(args.creation_time)
    time_diff = end_time - creation_time

    job_fail_count, retry_count = find_retries_failures(args.failures)
    success_count = args.task_count - job_fail_count

    print(
        'parent_job: ',
        'job: ' + workflow_name,
        'job_id: 123456',
        'success: ' + str(success_count),
        'retry_count: ' + str(retry_count),
        'job_count: ' + str(args.task_count),
        'job_failed_count: ' + str(job_fail_count),
        'start_time: ' + str(creation_time),
        'end_time: ' + str(end_time),
        'load_time ' + str(time_diff),
        'notes: ',
        sep='\n\r'
    )


def set_arguments():
    parser = argparse.ArgumentParser('Record workflow stats')
    parser.add_argument('--workflow_name', type=str, help='Workflow Name')
    parser.add_argument('--task_count', type=int, help='Task Count')
    parser.add_argument('--creation_time', type=str, help='Workflow Creation Time')
    parser.add_argument('--failures', type=str, help='Job Failures')
    parser.add_argument('--tasks', type=str, help='DAG tasks')
    return parser.parse_args()


def get_name(name):
    name_parts = name.split('-')
    return name_parts[:len(name_parts) - 1].join('-')


def get_creation_time(time_str):
    str_split = time_str.split()
    date_split = [int(date) for date in str_split[0].split('-')]
    time_split = [int(time) for time in str_split[1].split(':')]
    return dt.datetime(date_split[0], date_split[1], date_split[2], time_split[0], time_split[1], time_split[2])


def find_retries_failures(failures):
    failures_json = json.loads(eval(failures))
    job_fail_count = 0
    retry_count = 0
    tasks = []
    for fail in failures_json:
        if fail.get('message').lower() == 'no more retries left':
            job_fail_count = job_fail_count + 1
        elif fail.get('message') != '':
            retry_count = retry_count + 1
            task = fail.get('displayName').split('(')[0]
            if task not in tasks:
                tasks.append(task)

    retry_count = retry_count - len(tasks)
    return job_fail_count, retry_count


if __name__ == '__main__':
    run()
