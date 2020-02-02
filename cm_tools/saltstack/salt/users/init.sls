storage:
  group.present:
    - gid: 7648
    - system: True

cloud:
  group.present:
    - gid: 7649
    - system: True

wheel:
  group.present:
    - gid: 7650
    - system: True

operations:
  user.present:
    - fullname: Operations
    - shell: /bin/bash
    - home: /home/operations
    - uid: 4000
    - groups:
      - wheel
      - storage
      - cloud

testuser:
  user.absent
