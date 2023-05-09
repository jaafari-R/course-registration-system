from datetime import time

schedules = [
    [ 1,  ['Monday', 'Wednesday', 'Friday'],    time(9, 0, 0), time(10, 30, 00),    '101', 1001 ],
    [ 2,  ['Tuesday', 'Thursday'],              time(14, 0, 0), time(15, 30, 0),    '102', 1002 ],
    [ 3,  ['Monday', 'Wednesday'],              time(10, 0, 0), time(11, 30, 0),    '103', 1003 ],
    [ 4,  ['Tuesday', 'Thursday'],              time(13, 0, 0), time(14, 30, 0),    '104', 1004 ],
    [ 5,  ['Monday', 'Wednesday', 'Friday'],    time(11, 0, 0), time(12, 30, 0),    '105', 1005 ],
    [ 6,  ['Tuesday', 'Thursday'],              time(10, 0, 0), time(11, 30, 0),    '106', 1006 ],
    [ 7,  ['Monday', 'Wednesday', 'Friday'],    time(14, 0, 0), time(15, 30, 0),    '107', 1007 ],
    [ 8,  ['Tuesday', 'Thursday'],              time(10, 0, 0), time(11, 30, 0),    '108', 1008 ],
    [ 9,  ['Monday', 'Wednesday'],              time(9, 0, 0), time(10, 30, 0),     '109', 1009 ],
    [ 10, ['Tuesday', 'Thursday'],              time(13, 0, 0), time(14, 30, 0),    '110', 1010 ],
    [ 11, ['Monday', 'Wednesday'],              time(11, 0, 0), time(12, 30, 0),    '111', 1011 ],
    [ 12, ['Tuesday', 'Thursday'],              time(10, 0, 0), time(11, 30, 0),    '112', 1012 ],
    [ 13, ['Monday', 'Wednesday'],              time(13, 0, 0), time(14, 30, 0),    '113', 1013 ],
    [ 14, ['Tuesday', 'Thursday'],              time(14, 0, 0), time(15, 30, 0),    '114', 1014 ],
    [ 15, ['Monday', 'Wednesday'],              time(9, 0, 0), time(10, 30, 0),     '115', 1015 ],
    [ 16, ['Tuesday', 'Thursday'],              time(13, 0, 0), time(14, 30, 0),    '116', 1016 ]
]

courses = [
    [1001, 'Introduction to Programming',       'An introduction to programming concepts and techniques',                       [],                 'Faisal',           50],
    [1002, 'Web Development',                   'Learn how to build and design dynamic web applications',                       [1001],             'Mohamad jabary',   40],
    [1003, 'Database Design',                   'Learn how to design and implement databases',                                  [1001],             'Ezdehar',          30],
    [1004, 'Mobile App Development',            'Learn how to build and design mobile applications',                            [1001],             'Raduan Tahbob',    35],
    [1005, 'Machine Learning',                  'Learn the fundamentals of machine learning and its applications',              [1001, 1003],       'Hashem Tamimi',    25],
    [1006, 'Artificial Intelligence',           'Explore the theories and techniques behind artificial intelligence',           [1001, 1003, 1005], 'Zain Salah',       20],
    [1007, 'Operating Systems',                 'Learn how operating systems work and their impact on computer performance',    [1001],             'Suzan Sultan',     30],
    [1008, 'Computer Networks',                 'Learn the principles and protocols of computer networking',                    [1001],             'Liana',            40],
    [1009, 'Computer Architecture',             'Learn how computer hardware and software interact',                            [1001],             'Faisal',           35],
    [1010, 'Software Engineering',              'Learn how to design and develop large-scale software systems',                 [1001],             'Mazen',            30],
    [1011, 'Algorithms and Data Structures',    'Learn the theory behind algorithms and data structures',                       [1006],             'Nabil',            25],
    [1012, 'Computer Graphics',                 'Learn how to create and manipulate digital images',                            [1001, 1003],       'Musa',             20],
    [1013, 'Computer Vision',                   'Learn how computers interpret and understand digital images and videos',       [1001, 1005],       'Hashem',           15],
    [1014, 'Natural Language Processing',       'Learn how computers process and understand human language',                    [1001, 1005],       'Musa',             20],
    [1015, 'Computer Security',                 'Learn how to protect computer systems and networks from attacks',              [1001, 1008],       'Manal',            25],
    [1016, 'Data Science',                      'Learn how to extract insights from large and complex datasets',                [1001, 1005],       'zain ',            23]
]