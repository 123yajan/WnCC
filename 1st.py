# Define the skill names and their positions in the skill levels list
skill_names = ['HTML', 'Python', 'DSA', 'Java', 'SQL']
skill_positions = {skill_names[i]: i for i in range(len(skill_names))}

# Read the number of participants and their skills
n = int(input())
participants = {}
for i in range(n):
    line = input().split()
    roll_number = line[0]
    skill_levels = [int(x) for x in line[1:]]
    participants[roll_number] = skill_levels

# Read the number of projects and their skill requirements
m = int(input())
projects = []
for i in range(m):
    line = input().split()
    name = line[0]
    skill_levels = [int(x) for x in line[1:]]
    roles = []
    for j in range(len(skill_levels)):
        if skill_levels[j] > 0:
            skill_name = skill_names[j]
            role = {'skill_name': skill_name, 'required_level': skill_levels[j], 'mentors': []}
            roles.append(role)
    project = {'name': name, 'roles': roles}
    projects.append(project)

# Check if a participant has the required skill set for a role
def has_skill_set(skill_set, role):
    skill_name = role['skill_name']
    required_level = role['required_level']
    level = skill_set[skill_positions[skill_name]]
    return level >= required_level
# Check if a participant can mentor another participant for a role
def can_mentor(skill_set, role, mentors):
    skill_name = role['skill_name']
    required_level = role['required_level']
    for mentor in mentors:
        if mentor['skill_name'] == skill_name and mentor['level']== required_level+1:
            return True
    return False
# Process each project and count the completed projects
completed_projects = 0
for project in projects:
    roles = project['roles']
    for i in range(len(roles)):
        role = roles[i]
        required_skill_set = [0] * len(skill_names)
        required_skill_set[skill_positions[role['skill_name']]] = role['required_level']
        mentors = []
        for j in range(len(roles)):
            if j != i:
                other_role = roles[j]
                if other_role['required_level'] > 0:
                    for roll_number, skill_set in participants.items():
                        if has_skill_set(skill_set, other_role):
                            if can_mentor(skill_set, role, mentors):
                                mentors.append({'roll_number': roll_number, 'skill_name': other_role['skill_name'], 'level': skill_set[skill_positions[other_role['skill_name']]]})
                                print(mentors)
                                break
        for roll_number, skill_set in participants.items():
            if has_skill_set(skill_set, role) or can_mentor(skill_set, role, mentors):
                completed_projects += 1
                break
# Output the number of completed projects
print(completed_projects)