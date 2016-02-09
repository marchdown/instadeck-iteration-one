drop table if exists decks;
create table decks (
  id integer primary key autoincrement,
  slug text,
  title text not null,
  'content' text not null
);

insert into decks values (1, "e244aa", "imma_deck", '''foo
bar''');

insert into decks(slug, title, content)  values ("c1c305", "imma_deck2", '''baz
quux''');
insert into decks(slug, title, content)  values ("e5fe8e", "imma_deck3", '''bar baz
quux foo''');
