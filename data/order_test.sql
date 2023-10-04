SELECT * FROM taipei_travel.order;
Insert into taipei_travel.order (order_price, prime, status, number, contact_name, contact_email, contact_phone, user_id) values (2500, "test", 1, 1,"name", "email", "8888", 20);

Delete from taipei_travel.order where id = 15;

update taipei_travel.order set status = 2 where id = 27 and user_id = 9;

Select distinct o.id, o.number, o.order_price, o.contact_name, o.contact_email, o.contact_phone, o.status, o.user_id ,b.id  as booking_id,b.attraction_id, b.date, b.time, a.address, group_concat(distinct i.src separator ',') from taipei_travel.order o left join taipei_travel.booking b on o.id = b.order_id left join taipei_travel.attraction a on b.attraction_id = a.id left join taipei_travel.image i on a.id = i.attraction_id where o.number = "D202310050gLsLG" and o.user_id = 20 group by o.id, b.id;