import requests
import json

# 随手写的 目前只针对2024版
# examPlanId: "b56e5bfe-d0eb-446b-8cfe-e87da2608c75" 考试项目ID
# 'userExamPlanId': '620145a3-468b-4a65-bc73-4e484e3cfad2' 进入考试一个ID
# userExamId: 7ab01ffe-0caa-4689-a29b-332d26aeb001 考完一次一个ID

# 考过一遍 题库固定 每个人题目不一样 但是考过一次就固定 每天题目不一样（目前暂时发现的机制）
# 所以运行两遍即可怕程序一键满分

# 运行之前一定填写好下面的参数
userId = ''  #用户ID
tenantCode = 0  # 学校Code
x_token = '' #校验
userExamPlanId = '' # 开始考试后当前考试ID

headers = {
    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.139 Safari/537.36',
    'x-token': f'{x_token}'  # 关键参数token
}

# 懒得写了 F12吧 后续有时间再完善
def get_tenantCode(schoolName):
    url = 'https://weiban.mycourse.cn/pharos/login/getTenantListWithLetter.do?timestamp=1713318535.868'

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.139 Safari/537.36',
        'x-token': f'{x_token}'
    }

    schoolList = []
    Code = ''

    r = requests.post(url, headers=headers)
    data = json.loads(r.text)['data']
    for i in data:
        l = i['list']
        schoolList = schoolList + l
    for school in schoolList:
        if school['name'] == schoolName:
            Code = school['code']
            break
    return Code

# 懒得写了 F12吧 后续有时间再完善
# def get_userID_token():
#     url = 'https://weiban.mycourse.cn/pharos/login/login.do?timestamp=1713319251.071'



def get_questions_answers():
    url = 'https://weiban.mycourse.cn/pharos/exam/reviewPaper.do?timestamp=1713257613.996'
    data = {
        'tenantCode': f'{tenantCode}',
        'userId': f'{userId}',
        'userExamId': '8b3a6946-a1d6-4035-9bcf-db269dab677d',
        'isRetake': 2
    }

    r = requests.post(url, data=data, headers=headers)

    content = json.loads(r.text)['data']['questions']

    questions_answers = {}
    questions_titles = []

    for question in content:
        questions_titles.append(question['title'])
        answers = []
        optionList = question['optionList']
        for i in optionList:
            if i['isCorrect'] == 1:
                answers.append(i['id'])
        questions_answers[question['id']] = answers

    # questions_titles.sort()
    # print(questions_titles)

    return questions_answers


def get_questions_List():
    url = 'https://weiban.mycourse.cn/pharos/exam/startPaper.do?timestamp=1713258253.05'
    data = {
        'tenantCode': f'{tenantCode}',
        'userId': f'{userId}',
        'userExamPlanId': f'{userExamPlanId}'
    }

    r = requests.post(url, data=data, headers=headers)

    content = json.loads(r.text)['data']['questionList']

    new_ids = []

    questions_titles = []

    for question in content:
        questions_titles.append(question['title'])
        new_ids.append(question['id'])
    # print(content)

    # questions_titles.sort()
    # print(questions_titles)
    return new_ids


def recordQuestion(questionId, answerIds):
    url = 'https://weiban.mycourse.cn/pharos/exam/recordQuestion.do?timestamp=1713258614.138'

    data = {
        'tenantCode': f'{tenantCode}',
        'userId': f'{userId}',
        'userExamPlanId': f'{userExamPlanId}',

        'questionId': f'{questionId}',
        'useTime': 3600,
        'answerIds': f'{answerIds}',

        'examPlanId': 'b56e5bfe-d0eb-446b-8cfe-e87da2608c75'
    }

    r = requests.post(url, data=data, headers=headers)
    content = json.loads(r.text)
    print(content)


def submit():
    url = 'https://weiban.mycourse.cn/pharos/exam/submitPaper.do?timestamp=1713262229.987'
    data = {
        'tenantCode': f'{tenantCode}',
        'userId': f'{userId}',
        'userExamPlanId': f'{userExamPlanId}'
    }

    r = requests.post(url, data=data, headers=headers)
    content = json.loads(r.text)
    print(content)


if __name__ == '__main__':
    # tenantCode = get_tenantCode('XXX大学')
    #
    # print(tenantCode)

    questions_answers = get_questions_answers()
    # print(questions_answers)
    # 假设已经答完一次题，得到题库答案
#     questions_answers = {'0a98a540-6657-4770-be97-813e6e35e04a': ['ff5769f8-8fdc-11ed-a45a-6805cab01fc0'], '34e1ce08-01a4-4a2b-9508-5f26c8d7f7a3': ['ff29cac5-8fdc-11ed-a45a-6805cab01fc0'], '1b720d7c-5b26-44c6-b73a-794983940ee4': ['eb6c869b-798f-4f9b-bb11-97cd4abccb6e'], 'd0ae3d7c-3f95-4a5f-9300-931b734e69a1': ['b01ddab6-eb17-40e1-991e-36d587647395'], '29691168-f32d-4da6-81a1-2e0f9efb7da1': ['c6de8f1e-5c3f-4b40-b1b8-3dd6b6ab5f0b'], '9123da81-6d74-4fa4-9444-7562fc88e5e5': ['b9f37631-4a5d-4fab-a610-3d7c94e4937b'], 'b1fb5d4f-fedb-4382-b6d7-1fa27e5986c6': ['9ef8a3d1-e3c3-40d1-93c5-93008e1df6fa'], '34586a73-0523-4bdf-bf4d-5edc6ed0e726': ['ff6b2aee-8fdc-11ed-a45a-6805cab01fc0'], '4874bf3c-c288-4dbf-b480-9ada3a5a2171': ['ff2f2f6a-8fdc-11ed-a45a-6805cab01fc0'], '517fea30-9c48-4dc2-8fca-8824f8ff77d3': ['f3e53e3e-8bb4-42e1-8dac-9efa1872edc1'], 'cf6431cd-9ffd-4da5-87f4-f605eb40762d': ['ff7fed15-8fdc-11ed-a45a-6805cab01fc0'], '8f5cbd82-8aa8-4123-a7c3-90c5d6fbb533': ['ff6da3cf-8fdc-11ed-a45a-6805cab01fc0'], '07106ccf-9c97-45df-a934-7dde4b65186f': ['ff71fa1a-8fdc-11ed-a45a-6805cab01fc0'], '5c002f51-d1c9-4cee-8304-cf7767f93504': ['ff84a88f-8fdc-11ed-a45a-6805cab01fc0'], '61979196-b526-49cb-ac21-90c99aead693': ['ff58861f-8fdc-11ed-a45a-6805cab01fc0'], '83b315bf-0326-454c-9002-01c1fd77f997': ['ff92a6db-8fdc-11ed-a45a-6805cab01fc0'], '74a2ef73-34e1-4501-9cb8-f6053bbe0121': ['ff6edc0f-8fdc-11ed-a45a-6805cab01fc0'], 'd41db501-18c9-4585-80db-3d924c552036': ['ff24ccb8-8fdc-11ed-a45a-6805cab01fc0'], 'eb8a947c-9bf6-45c3-a5e4-065f49b7f5b5': ['f5f4bd33-3cbe-49e1-a850-010f9c7a5ce8'], '8b2bd91c-aed6-448c-972c-4d0a8453f1d6': ['ff35839d-8fdc-11ed-a45a-6805cab01fc0'], 'c490d4e0-45d7-48bb-8718-b966099d987f': ['ff7f86d3-8fdc-11ed-a45a-6805cab01fc0'], '76ddb6fe-6e96-40e9-b5aa-a055964133cb': ['33edf5e2-ff1d-4f32-816a-4dc4aca9913d'], '4211abbf-d7ca-4333-8295-0749ac890e9e': ['ff2fc11e-8fdc-11ed-a45a-6805cab01fc0'], '51c23a49-e980-4e89-9d74-2b3ace7356b8': ['ff4e1f6d-8fdc-11ed-a45a-6805cab01fc0'], '62118f03-b87f-4dbe-a4bb-3592096aaef8': ['ff2a70b8-8fdc-11ed-a45a-6805cab01fc0'], '43b77ed3-dd33-46da-b6bc-63e3507a8c7f': ['9b1a5a83-4f20-4f4c-adc5-606dce9a28cc'], 'e617d1a0-1071-4d81-a435-516ca8cd1a59': ['ff698e2c-8fdc-11ed-a45a-6805cab01fc0'], '71d05f06-2161-45fc-8729-d3409e706fe2': ['ff5b8411-8fdc-11ed-a45a-6805cab01fc0'], '123d13de-0c4c-486f-8a96-08e5216da62f': ['ff221d90-8fdc-11ed-a45a-6805cab01fc0'], '33d82845-ee8e-4fde-bdd3-c639a82e3cd1': ['ff2657b9-8fdc-11ed-a45a-6805cab01fc0'], '2fd20706-2938-4fae-8e4c-04599436b88c': ['ff6444c8-8fdc-11ed-a45a-6805cab01fc0', 'ff7f13e1-8fdc-11ed-a45a-6805cab01fc0', 'ff681199-8fdc-11ed-a45a-6805cab01fc0', 'ff3d0014-8fdc-11ed-a45a-6805cab01fc0'], 'd147fa8d-00b7-46fa-8763-6fb20836e7cf': ['c9a72383-9157-4892-8ca6-337d3e55391c', '0e6f77b3-5d5a-45bd-bc92-94b63d51d1e8', '5de15705-d900-42d6-a4d8-30bcfd39a2d4'], 'f8ca218c-4a40-43a7-8d1a-8e9aa827cf50': ['ff24fc1d-8fdc-11ed-a45a-6805cab01fc0', 'ff571f7d-8fdc-11ed-a45a-6805cab01fc0', 'ff959c04-8fdc-11ed-a45a-6805cab01fc0'], '7e2c9946-33d2-4f43-88d1-afba9ddabb9e': ['e55f7497-62d0-4a3c-878e-e54e74b5b3ab', '9ee748bc-b9ab-4972-bc8a-105eb0a09eb5'], '826c163f-5d52-4c62-9588-fc5ad10adb38': ['852073bc-c78b-4967-b3e9-913eb05f54ae', 'd5cc5921-9bcd-4c63-ad25-75da7bf1b093'], 'a3796cbb-cea8-43b5-8ece-1c6c22caca35': ['ae44fae3-bc9c-4cb7-8c7c-26d8005ac56a', '7bc2d478-2fd5-4a85-82af-4a023cb9661e', 'cd9c1b0f-3e6a-4e5b-8459-b465d147c304'], 'd965e0f2-9415-4603-9bf0-0450a805b6ad': ['ff8e4961-8fdc-11ed-a45a-6805cab01fc0', 'ff5cae5d-8fdc-11ed-a45a-6805cab01fc0'], '92cfd096-6434-4db8-8fb6-efd7dea8a4f3': ['ff6dd543-8fdc-11ed-a45a-6805cab01fc0', 'ff9547b4-8fdc-11ed-a45a-6805cab01fc0', 'ff42a393-8fdc-11ed-a45a-6805cab01fc0'], 'cb867b09-aa8c-4caf-bc0c-ae34e7966db0': ['ff3025e8-8fdc-11ed-a45a-6805cab01fc0', 'ff3c131f-8fdc-11ed-a45a-6805cab01fc0'], '98877a18-0e1d-42f0-b01b-4da5eb42b164': ['ff968c74-8fdc-11ed-a45a-6805cab01fc0', 'ff938f4d-8fdc-11ed-a45a-6805cab01fc0', 'ff8f5ebc-8fdc-11ed-a45a-6805cab01fc0', 'ff38a7f6-8fdc-11ed-a45a-6805cab01fc0'], '48b52451-cf35-4050-8b09-aa0b652c9652': ['5d14c540-43ba-433e-8801-ec1024aff9a1', 'a152e77f-f0a0-4893-9d0e-d0079846b6ec', '1e5b6961-0c49-4baa-97f0-bf1330399f1f'], 'c8376622-c04f-4eae-b3a5-c6245ff18874': ['b56cc2a7-fad9-4425-914d-d12af7ed290e', '28bfa529-2fff-4532-8ee1-3d641b376900', '0220529d-688f-4402-8268-6b017424a218', '0cf99981-0b4c-4798-8220-6dd2f842103c'], 'b7c6f215-ea3c-41f5-8a80-79afe1171e31': ['2a63b45c-1831-42c9-beef-ac780f15b350', '562cbfe7-2acf-4e11-8bba-e017541e6cc0'], 'd62d1c92-c478-4fbb-9437-fce963099e35': ['9a47cff1-8e29-4bde-8dd6-17c24d50ff6c', 'fa8fca74-d1e9-499a-91a9-01990cb1b8d3'], '0848a9f3-bcdf-4a95-8acc-3fd26c5d1b28': ['ff961488-8fdc-11ed-a45a-6805cab01fc0', 'ff2ea50b-8fdc-11ed-a45a-6805cab01fc0'], '69899ca4-e1e7-46e1-9386-32bb5bb2136b': ['86796f26-f9a9-4e6c-a1ac-6ebde54f1bbd', '58c6e7f8-96f4-4884-8c09-e3889cc257b2'], 'd369d314-61a8-4965-b18b-e3a99a42b8dc': ['ff99dfb7-8fdc-11ed-a45a-6805cab01fc0', 'ff407274-8fdc-11ed-a45a-6805cab01fc0', 'ff30ea98-8fdc-11ed-a45a-6805cab01fc0'], '727b4327-f29d-4b89-b33f-cefdca822127': ['ff9a2637-8fdc-11ed-a45a-6805cab01fc0', 'ff8a0bbe-8fdc-11ed-a45a-6805cab01fc0', 'ff5aabf0-8fdc-11ed-a45a-6805cab01fc0'], 'c049a355-d41a-4256-815c-e287236c2093': ['ff82d40a-8fdc-11ed-a45a-6805cab01fc0', 'ff406f6f-8fdc-11ed-a45a-6805cab01fc0'], 'e45c4ce4-afc4-40a6-9979-539902ab4dc8': ['ff468b34-8fdc-11ed-a45a-6805cab01fc0', 'ff49446b-8fdc-11ed-a45a-6805cab01fc0', 'ff40c3b6-8fdc-11ed-a45a-6805cab01fc0']
# ,'0a98a540-6657-4770-be97-813e6e35e04a': ['ff5769f8-8fdc-11ed-a45a-6805cab01fc0'], '34e1ce08-01a4-4a2b-9508-5f26c8d7f7a3': ['ff29cac5-8fdc-11ed-a45a-6805cab01fc0'], '1b720d7c-5b26-44c6-b73a-794983940ee4': ['eb6c869b-798f-4f9b-bb11-97cd4abccb6e'], 'd0ae3d7c-3f95-4a5f-9300-931b734e69a1': ['b01ddab6-eb17-40e1-991e-36d587647395'], '29691168-f32d-4da6-81a1-2e0f9efb7da1': ['c6de8f1e-5c3f-4b40-b1b8-3dd6b6ab5f0b'], '9123da81-6d74-4fa4-9444-7562fc88e5e5': ['b9f37631-4a5d-4fab-a610-3d7c94e4937b'], 'b1fb5d4f-fedb-4382-b6d7-1fa27e5986c6': ['9ef8a3d1-e3c3-40d1-93c5-93008e1df6fa'], '34586a73-0523-4bdf-bf4d-5edc6ed0e726': ['ff6b2aee-8fdc-11ed-a45a-6805cab01fc0'], '4874bf3c-c288-4dbf-b480-9ada3a5a2171': ['ff2f2f6a-8fdc-11ed-a45a-6805cab01fc0'], '517fea30-9c48-4dc2-8fca-8824f8ff77d3': ['f3e53e3e-8bb4-42e1-8dac-9efa1872edc1'], 'cf6431cd-9ffd-4da5-87f4-f605eb40762d': ['ff7fed15-8fdc-11ed-a45a-6805cab01fc0'], '8f5cbd82-8aa8-4123-a7c3-90c5d6fbb533': ['ff6da3cf-8fdc-11ed-a45a-6805cab01fc0'], '07106ccf-9c97-45df-a934-7dde4b65186f': ['ff71fa1a-8fdc-11ed-a45a-6805cab01fc0'], '5c002f51-d1c9-4cee-8304-cf7767f93504': ['ff84a88f-8fdc-11ed-a45a-6805cab01fc0'], '61979196-b526-49cb-ac21-90c99aead693': ['ff58861f-8fdc-11ed-a45a-6805cab01fc0'], '83b315bf-0326-454c-9002-01c1fd77f997': ['ff92a6db-8fdc-11ed-a45a-6805cab01fc0'], '74a2ef73-34e1-4501-9cb8-f6053bbe0121': ['ff6edc0f-8fdc-11ed-a45a-6805cab01fc0'], 'd41db501-18c9-4585-80db-3d924c552036': ['ff24ccb8-8fdc-11ed-a45a-6805cab01fc0'], 'eb8a947c-9bf6-45c3-a5e4-065f49b7f5b5': ['f5f4bd33-3cbe-49e1-a850-010f9c7a5ce8'], '8b2bd91c-aed6-448c-972c-4d0a8453f1d6': ['ff35839d-8fdc-11ed-a45a-6805cab01fc0'], 'c490d4e0-45d7-48bb-8718-b966099d987f': ['ff7f86d3-8fdc-11ed-a45a-6805cab01fc0'], '76ddb6fe-6e96-40e9-b5aa-a055964133cb': ['33edf5e2-ff1d-4f32-816a-4dc4aca9913d'], '4211abbf-d7ca-4333-8295-0749ac890e9e': ['ff2fc11e-8fdc-11ed-a45a-6805cab01fc0'], '51c23a49-e980-4e89-9d74-2b3ace7356b8': ['ff4e1f6d-8fdc-11ed-a45a-6805cab01fc0'], '62118f03-b87f-4dbe-a4bb-3592096aaef8': ['ff2a70b8-8fdc-11ed-a45a-6805cab01fc0'], '43b77ed3-dd33-46da-b6bc-63e3507a8c7f': ['9b1a5a83-4f20-4f4c-adc5-606dce9a28cc'], 'e617d1a0-1071-4d81-a435-516ca8cd1a59': ['ff698e2c-8fdc-11ed-a45a-6805cab01fc0'], '71d05f06-2161-45fc-8729-d3409e706fe2': ['ff5b8411-8fdc-11ed-a45a-6805cab01fc0'], '123d13de-0c4c-486f-8a96-08e5216da62f': ['ff221d90-8fdc-11ed-a45a-6805cab01fc0'], '33d82845-ee8e-4fde-bdd3-c639a82e3cd1': ['ff2657b9-8fdc-11ed-a45a-6805cab01fc0'], '2fd20706-2938-4fae-8e4c-04599436b88c': ['ff6444c8-8fdc-11ed-a45a-6805cab01fc0', 'ff7f13e1-8fdc-11ed-a45a-6805cab01fc0', 'ff681199-8fdc-11ed-a45a-6805cab01fc0', 'ff3d0014-8fdc-11ed-a45a-6805cab01fc0'], 'd147fa8d-00b7-46fa-8763-6fb20836e7cf': ['c9a72383-9157-4892-8ca6-337d3e55391c', '0e6f77b3-5d5a-45bd-bc92-94b63d51d1e8', '5de15705-d900-42d6-a4d8-30bcfd39a2d4'], 'f8ca218c-4a40-43a7-8d1a-8e9aa827cf50': ['ff24fc1d-8fdc-11ed-a45a-6805cab01fc0', 'ff571f7d-8fdc-11ed-a45a-6805cab01fc0', 'ff959c04-8fdc-11ed-a45a-6805cab01fc0'], '7e2c9946-33d2-4f43-88d1-afba9ddabb9e': ['e55f7497-62d0-4a3c-878e-e54e74b5b3ab', '9ee748bc-b9ab-4972-bc8a-105eb0a09eb5'], '826c163f-5d52-4c62-9588-fc5ad10adb38': ['852073bc-c78b-4967-b3e9-913eb05f54ae', 'd5cc5921-9bcd-4c63-ad25-75da7bf1b093'], 'a3796cbb-cea8-43b5-8ece-1c6c22caca35': ['ae44fae3-bc9c-4cb7-8c7c-26d8005ac56a', '7bc2d478-2fd5-4a85-82af-4a023cb9661e', 'cd9c1b0f-3e6a-4e5b-8459-b465d147c304'], 'd965e0f2-9415-4603-9bf0-0450a805b6ad': ['ff8e4961-8fdc-11ed-a45a-6805cab01fc0', 'ff5cae5d-8fdc-11ed-a45a-6805cab01fc0'], '92cfd096-6434-4db8-8fb6-efd7dea8a4f3': ['ff6dd543-8fdc-11ed-a45a-6805cab01fc0', 'ff9547b4-8fdc-11ed-a45a-6805cab01fc0', 'ff42a393-8fdc-11ed-a45a-6805cab01fc0'], 'cb867b09-aa8c-4caf-bc0c-ae34e7966db0': ['ff3025e8-8fdc-11ed-a45a-6805cab01fc0', 'ff3c131f-8fdc-11ed-a45a-6805cab01fc0'], '98877a18-0e1d-42f0-b01b-4da5eb42b164': ['ff968c74-8fdc-11ed-a45a-6805cab01fc0', 'ff938f4d-8fdc-11ed-a45a-6805cab01fc0', 'ff8f5ebc-8fdc-11ed-a45a-6805cab01fc0', 'ff38a7f6-8fdc-11ed-a45a-6805cab01fc0'], '48b52451-cf35-4050-8b09-aa0b652c9652': ['5d14c540-43ba-433e-8801-ec1024aff9a1', 'a152e77f-f0a0-4893-9d0e-d0079846b6ec', '1e5b6961-0c49-4baa-97f0-bf1330399f1f'], 'c8376622-c04f-4eae-b3a5-c6245ff18874': ['b56cc2a7-fad9-4425-914d-d12af7ed290e', '28bfa529-2fff-4532-8ee1-3d641b376900', '0220529d-688f-4402-8268-6b017424a218', '0cf99981-0b4c-4798-8220-6dd2f842103c'], 'b7c6f215-ea3c-41f5-8a80-79afe1171e31': ['2a63b45c-1831-42c9-beef-ac780f15b350', '562cbfe7-2acf-4e11-8bba-e017541e6cc0'], 'd62d1c92-c478-4fbb-9437-fce963099e35': ['9a47cff1-8e29-4bde-8dd6-17c24d50ff6c', 'fa8fca74-d1e9-499a-91a9-01990cb1b8d3'], '0848a9f3-bcdf-4a95-8acc-3fd26c5d1b28': ['ff961488-8fdc-11ed-a45a-6805cab01fc0', 'ff2ea50b-8fdc-11ed-a45a-6805cab01fc0'], '69899ca4-e1e7-46e1-9386-32bb5bb2136b': ['86796f26-f9a9-4e6c-a1ac-6ebde54f1bbd', '58c6e7f8-96f4-4884-8c09-e3889cc257b2'], 'd369d314-61a8-4965-b18b-e3a99a42b8dc': ['ff99dfb7-8fdc-11ed-a45a-6805cab01fc0', 'ff407274-8fdc-11ed-a45a-6805cab01fc0', 'ff30ea98-8fdc-11ed-a45a-6805cab01fc0'], '727b4327-f29d-4b89-b33f-cefdca822127': ['ff9a2637-8fdc-11ed-a45a-6805cab01fc0', 'ff8a0bbe-8fdc-11ed-a45a-6805cab01fc0', 'ff5aabf0-8fdc-11ed-a45a-6805cab01fc0'], 'c049a355-d41a-4256-815c-e287236c2093': ['ff82d40a-8fdc-11ed-a45a-6805cab01fc0', 'ff406f6f-8fdc-11ed-a45a-6805cab01fc0'], 'e45c4ce4-afc4-40a6-9979-539902ab4dc8': ['ff468b34-8fdc-11ed-a45a-6805cab01fc0', 'ff49446b-8fdc-11ed-a45a-6805cab01fc0', 'ff40c3b6-8fdc-11ed-a45a-6805cab01fc0']}

    questions = get_questions_List()

    print(len(set(questions_answers.keys()) & set(questions))) # 题库有答案数量

    # for question in questions:
    #     if question not in questions_answers:
    #         continue
    #     recordQuestion(question, ','.join(questions_answers[question]))
    #
    # submit()
