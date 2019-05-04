

DROP TABLE IF EXISTS `app`;

CREATE TABLE `app` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `download` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `version` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `type` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `releaseTime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;


DROP TABLE IF EXISTS `chapter_1`;

CREATE TABLE `chapter_1` (
  `novelId` int(11) NOT NULL,
  `chapterId` int(11) NOT NULL,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `source` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '目标url',
  `content` blob,
  `sourceid` int(2) DEFAULT NULL COMMENT '来源',
  `flag` int(1) DEFAULT '0' COMMENT '0：未更新内容，1:更新了',
  PRIMARY KEY (`novelId`,`chapterId`) USING BTREE,
  KEY `index_novelId` (`novelId`) USING BTREE,
  KEY `chapter_flag_idx` (`flag`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

DROP TABLE IF EXISTS `chapter_2`;

CREATE TABLE `chapter_2` (
  `novelId` int(11) NOT NULL,
  `chapterId` int(11) NOT NULL,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `source` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '目标url',
  `content` blob,
  `sourceid` int(2) DEFAULT NULL COMMENT '来源',
  `flag` int(1) DEFAULT '0' COMMENT '0：未更新内容，1:更新了',
  PRIMARY KEY (`novelId`,`chapterId`) USING BTREE,
  KEY `index_novelId` (`novelId`) USING BTREE,
  KEY `chapter_flag_idx` (`flag`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

DROP TABLE IF EXISTS `dictionary`;

CREATE TABLE `dictionary` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `type` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `status` int(11) DEFAULT '0',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;


DROP TABLE IF EXISTS `message`;

CREATE TABLE `message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `feedbackUserId` int(11) DEFAULT NULL COMMENT '反馈用户id',
  `feedback` text CHARACTER SET utf8 COLLATE utf8_general_ci,
  `feedbackTime` int(11) DEFAULT NULL,
  `reply` text CHARACTER SET utf8 COLLATE utf8_general_ci,
  `replyTime` int(11) DEFAULT NULL,
  `replyUserId` int(11) DEFAULT NULL COMMENT '回复用户id',
  `read` tinyint(4) DEFAULT NULL COMMENT '0未读1已读',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `index_feedback_user` (`feedbackUserId`,`read`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;


DROP TABLE IF EXISTS `novel`;

CREATE TABLE `novel` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT ' ',
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `author` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `introduction` varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '简介',
  `recentChapterUpdateId` int(11) NOT NULL DEFAULT '0' COMMENT '最近更新章节id',
  `source` varchar(100) NOT NULL COMMENT '来源地址',
  `tagid` int(11) DEFAULT NULL COMMENT '类别',
  `cover` mediumblob,
  `status` int(2) DEFAULT '0' COMMENT '状态上新热门',
  `sourceid` int(2) DEFAULT '1' COMMENT '来源id',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `index_name_author` (`name`,`author`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;


DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nick` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `pwd` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `lastLoginTime` int(11) DEFAULT NULL COMMENT '最后一次登录时间',
  `phone` int(11) DEFAULT NULL,
  `email` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `deviceID` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `registerTime` int(11) DEFAULT NULL,
  `goldenBean` int(11) DEFAULT '0',
  `expireDate` int(11) DEFAULT NULL COMMENT '过期时间',
  `signInTime` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '' COMMENT '签到时间字符串',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `index_email` (`email`) USING BTREE,
  UNIQUE KEY `index_phone` (`phone`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

