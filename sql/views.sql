CREATE INDEX idx_games_developer_id ON games(developer_id);
CREATE INDEX idx_games_genre_id ON games(genre_id);
CREATE INDEX idx_games_platform_id ON games(platform_id);

CREATE INDEX idx_purchases_player_id ON purchases(player_id);
CREATE INDEX idx_purchases_game_id ON purchases(game_id);
CREATE INDEX idx_purchases_date ON purchases(purchase_date);

CREATE INDEX idx_reviews_game_id ON reviews(game_id);
CREATE INDEX idx_reviews_player_id ON reviews(player_id);

CREATE INDEX idx_sessions_game_id ON play_sessions(game_id);
CREATE INDEX idx_sessions_player_id ON play_sessions(player_id);
CREATE INDEX idx_sessions_date ON play_sessions(session_date);