original_id = ObjectId()

db.company.insert({
    "_id": original_id,
    "name": "Cisco",
    "url": "cisco.example.net"
})

db.users.insert({
    "name": "user1",
    "company_id": original_id,
    "ip":  "127.0.0.1"
})

db.company.insert({
    "_id": original_id,
    "name": "Verizon",
    "url": "verizon.example.net"
})

db.users.insert({
    "name": "user2",
    "company_id": original_id,
    "ip":  "127.0.0.2"
})

db.company.insert({
    "_id": original_id,
    "name": "AT&T",
    "url": "cisco.example.net"
})

db.users.insert({
    "name": "user3",
    "company_id": original_id,
    "ip":  "127.0.0.3"
})
