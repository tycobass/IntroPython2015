import culture_filter as cf

def test_recommender():
    r = cf.Recommender()
    assert r.medium == 'all'
    assert r.filename == 'all_mediums.txt'
    assert type(r.recommendations) == dict

# def test_recommender_load_data():
#     r = cf.Recommender()
#     r.filename = 'text.txt'
#     data = 'test data'
#     with open(r.filename, 'w') as outfile:
#         outfile.write(data)

#     assert f == r.recommendations
