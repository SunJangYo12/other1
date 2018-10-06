#!/bin/bash

<<EOF mysql -u root;
use otak;
insert into memori values('ping_destroy','');
EOF