import blizzy

members = blizzy.guild_presenter.get_guild_members("Botany Bay", "Executus", max_level_only=True)
for m in members:
    print(m.name)