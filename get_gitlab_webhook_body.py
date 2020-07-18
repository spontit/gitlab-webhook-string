def get_gitlab_webhook_body(payload):
    result = str()

    # Get Event Info
    if payload.get('event_name'):
        result += f"Event Name: {payload['event_name']}\n"
    if payload.get('event_type'):
        result += f"Event Type: {payload['event_type']}\n"
    if payload.get('user_name'):
        result += f"Acting User: {payload['user_name']}\n"
    if payload.get('object_kind'):
        result += f"Object Kind: {payload['object_kind']}\n"

    # Get Project Info
    if payload.get('project'):
        project = payload['project']
        if project.get('name'):
            project_name = project['name']
            result += f"Project Name: {project_name}\n"

    # Get Repository Info
    if payload.get('repository'):
        repository = payload['repository']
        if repository.get('name'):
            repository_name = repository['name']
            result += f"Repository Name: {repository_name}\n"

    # Get Wiki Content
    wiki = payload.get('wiki')
    if wiki:
        wiki_web_url = wiki.get('web_url')
        if wiki_web_url:
            result += f"Wiki URL: {wiki_web_url}\n"

    # Get Commits
    commits = payload.get('commits', list())
    for commit in commits:
        commit_message = commit.get('message')
        commit_title = commit.get('title')
        commit_time = commit.get('timestamp')
        commit_url = commit.get('url')
        commit_author_name = commit.get('author', dict()).get('name')
        if commit_message and commit_title and commit_time and commit_url and commit_author_name:
            result += "New Commit"
            result += f"\n\tTitle: {commit_title}"
            result += f"\n\tMessage: {commit_message}"
            result += f"\n\tTime: {commit_time}"
            result += f"\n\tAuthor: {commit_author_name}"
            result += f"\n\tURL: {commit_url}"

    # Get Object: Works for commits, issues, wiki, notes
    object_attributes = payload.get('object_attributes')
    if object_attributes:
        result += "\nObject"
        object_title = object_attributes.get('title')
        object_action = object_attributes.get('action')
        object_description = object_attributes.get('description')
        object_time_stamp = object_attributes.get('created_at')
        object_url = object_attributes.get('url')
        object_message = object_attributes.get('message')

        if object_title:
            result += f"\n\tTitle: {object_title}"
        if object_action:
            result += f"\n\tAction: {object_action}"
        if object_time_stamp:
            result += f"\n\tCreated At: {object_time_stamp}"
        if object_description:
            result += f"\n\tDescription: {object_description}"
        if object_message:
            result += f"\n\tMessage: {object_message}"
        if object_url:
            result += f"\n\tURL: {object_url}\n"

    # Get Job Info
    def add_build_to_result(build_payload, is_single_build):
        build_str = str()
        build_name = build_payload.get("build_name" if is_single_build else "name")
        if build_name:
            build_str += "\n\nBuild"
            build_str += f"\n\tName: {build_name}"
            build_stage = build_payload.get("build_stage" if is_single_build else "stage")
            build_status = build_payload.get("build_status" if is_single_build else "status")
            if build_stage:
                build_str += f"\n\tStage: {build_stage}"
            if build_status:
                build_str += f"\n\tStatus: {build_status}"

            created_at = build_payload.get('created_at')
            if created_at:
                build_str += f"\n\tCreated At: {created_at}"
        return build_str

    result += add_build_to_result(payload, True)
    builds = payload.get('builds', list())
    if type(builds) == list:
        for build in builds:
            result += add_build_to_result(build, False)

    return result
