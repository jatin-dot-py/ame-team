from knowledgebase.experts.ama_expert.job_codes import job_codes


# Workflow Script! Do not modify or move the path

def print_data_as_dict(csv_file_path):
    with open(csv_file_path, 'r') as file:
        csv_data = file.read()

    data_dict = {}
    lines = csv_data.split('\n')

    for line in lines:
        parts = line.split(',')
        if len(parts) == 3:
            group = parts[0]
            occupation = parts[1]
            industry = parts[2]

            if group not in data_dict:
                data_dict[group] = []

            data_dict[group].append({
                                        occupation: industry
                                        })

    dict_as_string = "job_codes = " + repr(data_dict)

    with open('job_codes.py', 'w') as file:
        file.write(dict_as_string)


def get_organized_job_codes():
    formatted_data = []
    for group, occupations in job_codes.items():
        group_info = f"Group {group}:"
        occupations_info = []
        for occupation in occupations:
            for job, industry in occupation.items():
                occupations_info.append(f"- {job}: {industry}")
        formatted_group_info = group_info + "\n" + "\n".join(occupations_info)
        formatted_data.append(formatted_group_info)
    return "\n\n".join(formatted_data)


if __name__ == '__main__':
    csv_file_path = r"D:\OneDrive\Downloads\PDR - Sheet5.csv"
    # print_data_as_dict(csv_file_path)

    formatted_data = get_organized_job_codes()
    print(formatted_data)
