SELECT * FROM taipei_travel.order;
Insert into taipei_travel.order (order_price, prime, status, number, contact_name, contact_email, contact_phone, user_id) values (2500, "test", 1, 1,"name", "email", "8888", 20);

Delete from taipei_travel.order where id = 15;

update taipei_travel.order set status = 2 where id = 27 and user_id = 9;