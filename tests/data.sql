truncate posts, users restart identity cascade;

insert into users (username, password)
values
  ('test',  'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
  ('other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79'),
  ('user3', 'pbkdf2:sha256:600000$MRvKki7rzhDOC0cK$05fc5af8d0d8cb7c3ac6fdb010e2724e74e7a8e43009c82ec8dde5597e649f41')
;

insert into posts (title, body, author_id, created)
values
  ('test title', 'test' || E'\n' || 'body', 1, '2023-01-01 00:00:00')
;
