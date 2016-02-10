drop table if exists decks;
create table decks (
  id integer primary key autoincrement,
  slug text,
  title text not null,
  'content' text not null
);

insert into decks values (1, "e244aa", "imma_deck", '''foo
bar''');

insert into decks(slug, title, content)  values ("multitude", "Among The Multitude by Walt Whitman", 'Among the men and women the multitude,
I perceive one picking me out by secret and divine signs,
Acknowledging none else, not parent, wife, husband, brother, child, any nearer than I am,
Some are baffled, but that one is not—that one knows me.
Ah lover and perfect equal,
I meant that you should discover me so by faint indirections,
And I when I meet you mean to discover you by the like in you.
');
insert into decks(slug, title, content)  values ("e5fe8e", "imma_deck3", '''bar baz
quux foo''');
