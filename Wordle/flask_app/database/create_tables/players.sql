CREATE TABLE IF NOT EXISTS `players` (
`entry_id`         int(11)  	   NOT NULL auto_increment	  COMMENT 'the id of this user',
`email`           varchar(100) NOT NULL            		  COMMENT 'the email',
`word`            varchar(100) NOT NULL            		  COMMENT 'word that they are guessing',
`score`           int(11)            		              COMMENT 'number of attempts it took to guess the word',

PRIMARY KEY (`entry_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Contains site player information";