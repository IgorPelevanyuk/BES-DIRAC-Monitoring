use SAMDB;
INSERT INTO Sites ( `name`) VALUES ( 'BES.GUCAS.cn');
INSERT INTO Sites ( `name`) VALUES ( 'BES.IHEP-PBS.cn');
INSERT INTO Sites ( `name`) VALUES ( 'BES.JINR.ru');
INSERT INTO Sites ( `name`) VALUES ( 'BES.PKU.cn');
INSERT INTO Sites ( `name`) VALUES ( 'BES.UMN.us');
INSERT INTO Sites ( `name`) VALUES ( 'BES.USTC.cn');
INSERT INTO Sites ( `name`) VALUES ( 'BES.WHU.cn');
INSERT INTO Sites ( `name`) VALUES ( 'BOINC.IHEP.cn');

INSERT INTO Services ( `site_id`, `name`) VALUES ( 1, 'WMS');
INSERT INTO Services ( `site_id`, `name`) VALUES ( 2, 'WMS');
INSERT INTO Services ( `site_id`, `name`) VALUES ( 3, 'WMS');
INSERT INTO Services ( `site_id`, `name`) VALUES ( 4, 'WMS');
INSERT INTO Services ( `site_id`, `name`) VALUES ( 5, 'WMS');
INSERT INTO Services ( `site_id`, `name`) VALUES ( 6, 'WMS');
INSERT INTO Services ( `site_id`, `name`) VALUES ( 7, 'WMS');
INSERT INTO Services ( `site_id`, `name`) VALUES ( 8, 'WMS');

INSERT INTO Tests ( `name`, `executable`, `description`) VALUES ( 'WMS_send_test', 'WMS_test.py', 'Sends job to check if it can be done ');

INSERT INTO Tests_to_Services ( `test_id`, `service_id`, `state`, `last_run`, `timeout`) VALUES ( 1, 1, 'Finished', '2009-01-01 00:00:00', 3600);
INSERT INTO Tests_to_Services ( `test_id`, `service_id`, `state`, `last_run`, `timeout`) VALUES ( 1, 2, 'Finished', '2009-01-01 00:00:00', 3600);
INSERT INTO Tests_to_Services ( `test_id`, `service_id`, `state`, `last_run`, `timeout`) VALUES ( 1, 3, 'Finished', '2009-01-01 00:00:00', 3600);
INSERT INTO Tests_to_Services ( `test_id`, `service_id`, `state`, `last_run`, `timeout`) VALUES ( 1, 4, 'Finished', '2009-01-01 00:00:00', 3600);
INSERT INTO Tests_to_Services ( `test_id`, `service_id`, `state`, `last_run`, `timeout`) VALUES ( 1, 5, 'Finished', '2009-01-01 00:00:00', 3600);
INSERT INTO Tests_to_Services ( `test_id`, `service_id`, `state`, `last_run`, `timeout`) VALUES ( 1, 6, 'Finished', '2009-01-01 00:00:00', 3600);
INSERT INTO Tests_to_Services ( `test_id`, `service_id`, `state`, `last_run`, `timeout`) VALUES ( 1, 7, 'Finished', '2009-01-01 00:00:00', 3600);
INSERT INTO Tests_to_Services ( `test_id`, `service_id`, `state`, `last_run`, `timeout`) VALUES ( 1, 8, 'Finished', '2009-01-01 00:00:00', 3600);

INSERT INTO Results (`test_id`, `service_id`,`state`,`last_update`) VALUES (1,1, 'Success', NOW() );
INSERT INTO Results (`test_id`, `service_id`,`state`,`last_update`) VALUES (1,2, 'Success', NOW() );
INSERT INTO Results (`test_id`, `service_id`,`state`,`last_update`) VALUES (1,3, 'Success', NOW() );
INSERT INTO Results (`test_id`, `service_id`,`state`,`last_update`) VALUES (1,4, 'Success', NOW() );
INSERT INTO Results (`test_id`, `service_id`,`state`,`last_update`) VALUES (1,5, 'Success', NOW() );
INSERT INTO Results (`test_id`, `service_id`,`state`,`last_update`) VALUES (1,6, 'Success', NOW() );
INSERT INTO Results (`test_id`, `service_id`,`state`,`last_update`) VALUES (1,7, 'Success', NOW() );
INSERT INTO Results (`test_id`, `service_id`,`state`,`last_update`) VALUES (1,8, 'Success', NOW() );

INSERT INTO States (`service_id`, `test_id`, `result_id`) VALUES (1, 1, 1);
INSERT INTO States (`service_id`, `test_id`, `result_id`) VALUES (2, 1, 2);
INSERT INTO States (`service_id`, `test_id`, `result_id`) VALUES (3, 1, 3);
INSERT INTO States (`service_id`, `test_id`, `result_id`) VALUES (4, 1, 4);
INSERT INTO States (`service_id`, `test_id`, `result_id`) VALUES (5, 1, 5);
INSERT INTO States (`service_id`, `test_id`, `result_id`) VALUES (6, 1, 6);
INSERT INTO States (`service_id`, `test_id`, `result_id`) VALUES (7, 1, 7);
INSERT INTO States (`service_id`, `test_id`, `result_id`) VALUES (8, 1, 8);
 
