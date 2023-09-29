SELECT * FROM taipei_travel.booking;
Insert into taipei_travel.booking (date, time, price, booking_status, user_id, attraction_id) values ("2023-09-26","afternoon", 2500, 1, 20, 1);

SELECT i.attraction_id, b.id , a.name, a.address, b.date,b.time, b.price,GROUP_CONCAT(DISTINCT i.src SEPARATOR ',') as images FROM taipei_travel.user u left join taipei_travel.booking b on u.id = b.user_id left join taipei_travel.attraction a on a.id = b.attraction_id left join taipei_travel.image i on a.id = i.attraction_id where u.id = 20 AND b.booking_status = 1 group by b.id;

UPDATE taipei_travel.booking SET booking_status=0 where id = 3 and user_id= 20;
SELECT * FROM taipei_travel.booking;

SELECT i.attraction_id, b.id , a.name, a.address, b.date,b.time, b.price, GROUP_CONCAT(DISTINCT i.src SEPARATOR ',') as images FROM taipei_travel.user u left join taipei_travel.booking b on u.id = b.user_id left join taipei_travel.attraction a on a.id = b.attraction_id left join taipei_travel.image i on a.id = i.attraction_id where u.id = 20 AND b.booking_status = 1 and a.id = 1 and b.date="2023-09-26" and b.time="afternoon" group by b.id;
