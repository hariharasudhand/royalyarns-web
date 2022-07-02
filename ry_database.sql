CREATE TABLE RY_Enquiry_Header(  
    id int NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    Reg_no TEXT,
    mill TEXT,
    Customer TEXT,
    Marketing_Zone TEXT,
    Payment_Term TEXT,
    Narration TEXT,
    Reason_For_Non_Acception TEXT,
    Replied_From_the_mill TEXT,
    Acceptance_from_the_mill TEXT,
    Date TEXT,
    Email_Details TEXT,
    Mill_Rep TEXT,
    Status TEXT

);

CREATE TABLE RY_Enquiry_Items(  
    id int NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    Counts TEXT,
    Quality TEXT,
    Type TEXT,
    Blend TEXT,
    Shade TEXT,
    Shade_Ref TEXT,
    Depth TEXT,
    UOM TEXT,
    Quantity TEXT,
    Status TEXT,
    Reg_no TEXT,
    Amount character varying(200),
    Last_order TEXT,
    Rate character varying(200)

);

CREATE TABLE User_Details(  
    UserName TEXT,
    Password TEXT,
    Role TEXT,
    id integer

);

CREATE TABLE auth_group(  
    id integer,
    name character varying(150)

);

CREATE TABLE auth_group_permissions(  
    id integer,
    group_id integer,
    permission_id integer

);

CREATE TABLE auth_permission(  
    id integer,
    name character varying(255),
    content_type_id integer,
    codename character varying(100)

);

CREATE TABLE auth_user(  
    id integer,
    password character varying(128),
    last_login timestamp with time zone,
    is_superuser boolean,
    username character varying(150),
    first_name character varying(150),
    last_name character varying(150),
    email character varying(254), 
    is_staff boolean,
    is_active boolean,
    date_joined timestamp with time zone

);

CREATE TABLE auth_user_groups(  
    id integer,
    user_id integer,
    group_id integer

);

CREATE TABLE auth_user_user_permissions(  
    id integer,
    user_id integer,
    permission_id integer

);

CREATE TABLE django_admin_log(  
    id integer,
    action_time timestamp with time zone,
    object_id text,
    object_repr character varying(200),
    action_flag smallint,
    change_message text,
    content_type_id integer,
    user_id integer

);

CREATE TABLE django_content_type(  
    id integer,
    app_label character varying(100),
    model character varying(100)

);

CREATE TABLE django_migrations(  
    id integer,
    app character varying(255),
    name character varying(255),
    applied timestamp with time zone

);

CREATE TABLE django_session(  
    session_key character varying(40),
    session_data text,
    expire_date timestamp with time zone

);






