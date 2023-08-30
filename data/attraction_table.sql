Create table Attraction(
	id bigint primary key unique NOT NULL,
    name character(255) NOT NULL,
    category character(255) NOT NULL,
    description character(255) NOT NULL,
    address character(255) NOT NULL,
    transport character(255) NOT NULL,
    
);