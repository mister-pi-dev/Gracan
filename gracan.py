import csv
import glob


# Home menu
def home_menu():
    print('\nAvailable options:\n'
          '\n(1) Process single csv file'
          '\n(2) Process all csv files in current folder'
          '\n(3) Merge MCQ and SAQ csv files to calculate total grade'
          '\n(4) Exit\n')
    select_option = input('Enter 1, 2, 3 or 4: ')
    if select_option == '1':
        # Reformat single csv file
        file = input("Enter csv file name: ")
        formatter(file)
    elif select_option == '2':
        # Reformat all csv files in current folder
        all_files = glob.glob('*.csv')
        all_files_sliced = []
        item_counter = 0
        print('\nCSV FILES DETECTED IN CURRENT FOLDER:\n')
        for item in all_files:
            print('- ', item)
        for item in all_files:
            if '_CANVAS_UPLOAD' not in item:
                all_files_sliced.append(item)
        for item in all_files_sliced:
            if '.csv' in item:
                item = item[:-4]
                all_files_sliced[item_counter] = item
                item_counter += 1
        print('\nCSV FILES TO BE PROCESSED IN CURRENT FOLDER:\n')
        for item in all_files_sliced:
            print('- ', item + '.csv')
        for item in all_files_sliced:
            formatter(item)
    elif select_option == '3':
        csv_data = []
        row_counter = 0
        mcq_file = input('\nENTER MCQ FILENAME: ')
        mcq_data = formatter(mcq_file)
        if mcq_data != 'invalid':
            saq_file = input('\nENTER SAQ FILENAME: ')
            saq_data = formatter(saq_file)
            if saq_data != 'invalid':
                max_points = float(mcq_data[0]) + float(saq_data[0])
                mcq_scores = {}
                saq_scores = {}
                total_file = mcq_file + '_-_' + saq_file
                assignment_total = total_file + ' Total Score'
                for item in mcq_data[1]:
                    mcq_scores[item[1]] = [item[0], item[1], item[2], item[3], item[4]]
                for item in saq_data[1]:
                    saq_scores[item[1]] = [item[0], item[1], item[2], item[3], item[4]]
                total_scores = {}
                for key in mcq_scores:
                    total_scores[key] = [mcq_scores[key][0],
                                         mcq_scores[key][1],
                                         mcq_scores[key][2],
                                         mcq_scores[key][3],
                                         mcq_scores[key][4],
                                         saq_scores[key][4],
                                         null_grade(mcq_scores[key][4]) + null_grade(saq_scores[key][4])]
                for item in total_scores.values():
                    student = item[0]
                    sis_user_id = item[1]
                    sis_login_id = item[2]
                    section = item[3]
                    mcq_score = item[4]
                    saq_score = item[5]
                    total_score = item[6]
                    row_data = [student, sis_user_id, sis_login_id, section, mcq_score, saq_score, total_score]
                    csv_data.append(row_data)
                    row_counter += 1
                print('\nCREATING FILE:', total_file + '_CANVAS_UPLOAD.csv \nStudent count:', row_counter)
                with open(total_file + '_CANVAS_UPLOAD_TOTAL.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Student',
                                     'SIS User ID',
                                     'SIS Login ID',
                                     'Section',
                                     'MCQ Score',
                                     'SAQ Score',
                                     assignment_total])
                    writer.writerow(['    Points Possible', '', '', '', mcq_data[0], saq_data[0], max_points])
                    writer.writerows(csv_data)
            else:
                home_menu()
        else:
            home_menu()
    elif select_option == '4':
        print('\nNOW EXITING\n')
        exit()
    else:
        print('ERROR: INVALID OPTION SELECTED')


# Reformat function
def formatter(file):
    # Enter filename of csv file (excluding csv file extension)
    if '_CANVAS_UPLOAD' in file:
        print('\nNOT PROCESSING: THIS FILE IS ALREADY FORMATTED FOR CANVAS\n \nRETURNING TO MAIN MENU\n')
        return 'invalid'
    else:
        file_ext = file + '.csv'
        assignment = file
        try:
            print('\nPROCESSING DATA IN:', file_ext)
            with open(file_ext, newline='') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                header = next(csv_reader)
                row_counter = 0
                student_counter = 0
                csv_data = []
                sid_counter = []
                if header[6] == 'Version':
                    while True:
                        try:
                            max_points = int(input('ENTER MAXIMUM POINTS FOR THIS ASSIGNMENT: '))
                            break
                        except ValueError:
                            print('ERROR: YOU MUST ENTER AN INTEGER')
                else:
                    max_points = ''
                for row in csv_reader:
                    if header[6] != 'Version' and row_counter < 1:
                        max_points = row[6]
                    student = row[1] + ', ' + row[0]
                    sis_user_id = row[2]
                    sis_login_id = row[3].split('@')[0]
                    section = row[4]
                    score = row[5]
                    row_data = [student, sis_user_id, sis_login_id, section, score]
                    csv_data.append(row_data)
                    row_counter += 1
                    student_counter += 1
                    sid_counter.append(sis_user_id)
                    if sid_counter.count(sis_user_id) >= 2:
                        print('\nALERT - DUPLICATE ENTRY DETECTED FOR SID', sis_user_id,
                              '\nCHECK:', student, '(' + sis_user_id + ')', 'EMAIL ADDRESS IN GRADESCOPE CSV\n')
                        input('PRESS ENTER TO CONTINUE\n')
                        student_counter -= 1
                print('CREATING FILE:', assignment + '_CANVAS_UPLOAD.csv \nRecords processed:', row_counter,
                      '\nStudent count:', student_counter)
            with open(file + '_CANVAS_UPLOAD.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Student', 'SIS User ID', 'SIS Login ID', 'Section', assignment])
                writer.writerow(['    Points Possible', '', '', '', max_points])
                writer.writerows(csv_data)
                data = [max_points, csv_data]
                return data
        except FileNotFoundError:
            print('ERROR: ' + file + '.csv NOT FOUND')
            home_menu()


# Null grade bypass
def null_grade(item):
    try:
        if item == '':
            return ''
        else:
            score = float(item)
            return score
    except ValueError:
        print('ERROR: SCORE IS NOT A NUMERICAL FLOAT VALUE')

sign = r"""


_____/\\\\\\\\\\\\_____________________________________/\\\\\\\\\______________________________        
 ___/\\\//////////___________________________________/\\\////////_______________________________       
  __/\\\____________________________________________/\\\/________________________________________      
   _\/\\\____/\\\\\\\__/\\/\\\\\\\___/\\\\\\\\\_____/\\\______________/\\\\\\\\\_____/\\/\\\\\\___     
    _\/\\\___\/////\\\_\/\\\/////\\\_\////////\\\___\/\\\_____________\////////\\\___\/\\\////\\\__    
     _\/\\\_______\/\\\_\/\\\___\///____/\\\\\\\\\\__\//\\\______________/\\\\\\\\\\__\/\\\__\//\\\_   
      _\/\\\_______\/\\\_\/\\\__________/\\\/////\\\___\///\\\___________/\\\/////\\\__\/\\\___\/\\\_  
       _\//\\\\\\\\\\\\/__\/\\\_________\//\\\\\\\\/\\____\////\\\\\\\\\_\//\\\\\\\\/\\_\/\\\___\/\\\_ 
        __\////////////____\///___________\////////\//________\/////////___\////////\//__\///____\///__


"""
print(sign, "\nWELCOME TO THE 'GRADESCOPE TO CANVAS' CSV CONVERTER")
while True:
    home_menu()
