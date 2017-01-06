DECLARE
user_id bigint;
iterator int;
BEGIN

DROP TABLE IF EXISTS channels_by_duration;
DROP TABLE IF EXISTS tags_values;
DROP TABLE IF EXISTS average_ratings;
DROP TABLE IF EXISTS channel_values2;

CREATE TEMP TABLE channels_by_duration
  (
	channel_id bigint, 
	channel_name text,
	total_duration int
  )
  ON COMMIT DELETE ROWS;
CREATE TEMP TABLE tags_values
  (
	tag_id bigint, 
	tag_name text, 
	value_ int
  )
  ON COMMIT DELETE ROWS;
CREATE TEMP TABLE average_ratings
  (
	channel_id bigint, 
	channel_name text, 
	average_rating float
  )
  ON COMMIT DELETE ROWS;
CREATE TEMP TABLE channel_values2
  (
	channel_id bigint, 
	channel_name text, 
	stream_url text, 
	value_ float
  )
  ON COMMIT DELETE ROWS;
  
	/*Wczytaj usera po userName*/
	SELECT id INTO user_id
	FROM auth_user
	WHERE username = user_Name;

	/*Historia odsluchan po user_id i grupowanie po channel_id*/
	INSERT INTO channels_by_duration (channel_id, channel_name, total_duration)
	SELECT chn.id, chn.name, sum(his.duration) as "total_duration"
	FROM history his, channel chn
	WHERE his.person_id = user_id AND his.channel_id = chn.id
	GROUP BY chn.id, chn.name
	ORDER BY sum(his.duration) desc;
	
	/* Ladowanie tagow do tablicy tymczasowej */
	INSERT INTO tags_values(tag_id, tag_name, value_)
	SELECT id, name, 0
	FROM tag;

	/* Wypelnij wartosc tagow wg dlugosci odsluchan */
	WHILE (SELECT COUNT(*) FROM channels_by_duration) > 0 LOOP
	
		SELECT cbd.channel_id INTO iterator
		FROM channels_by_duration cbd
		LIMIT 1;

		UPDATE tags_values AS tv
		SET value_ = tv.value_ + cbd.total_duration
		FROM  channels_by_duration cbd, tags_channels tc
		WHERE tv.tag_id = tc.tag_id AND iterator = tc.channel_id;
		
		DELETE FROM channels_by_duration cbd
		WHERE cbd.channel_id = iterator;
		
	END LOOP;
		
	/* Zaladuj stacje do tablicy tymczasowej */
	INSERT INTO channel_values2(channel_id, channel_name, stream_url, value_)
	SELECT ch.id, ch.name, ch.stream_url, 0.0
	FROM channel ch;
	
	/* Wypelnij wartosc stacji wg wartosci tagow */

	
	WHILE (SELECT COUNT(*) FROM tags_values) > 0 LOOP

		SELECT tv.tag_id INTO iterator
		From tags_values tv
		LIMIT 1;

		UPDATE channel_values2 AS cv
		SET value_ = cv.value_ + tv.value_
		FROM tags_values tv, tags_channels tc
		WHERE iterator = tc.tag_id AND cv.channel_id = tc.channel_id;
		
		DELETE FROM tags_values tv
		WHERE tv.tag_id = iterator;

	END LOOP;
	
	/* Srednia ocena */
	INSERT INTO average_ratings (channel_id, channel_name, average_rating)
	SELECT chn.id, chn.name, AVG(Cast(r.value AS float))
	FROM channel chn, ratings r
	WHERE chn.id = r.channel_id
	GROUP BY chn.id, chn.name;

	/* Srednia wartosc na 5/10 dla tych bez ocen */
	INSERT INTO average_ratings (channel_id, channel_name, average_rating)
	SELECT chn.id, chn.name, 5.0
	FROM channel chn
	WHERE chn.id NOT IN (SELECT ar.channel_id from average_ratings ar);
	
	/* Pomnoz wartosc stacji przez srednia ocene */
	UPDATE channel_values2 AS cv
	SET value_ = cv.value_ * ar.average_rating / 10.0
	FROM average_ratings ar
	WHERE cv.channel_id = ar.channel_id;
	
	/* Wybierz najlepsze 3 */
	RETURN QUERY SELECT cv.channel_id, cv.channel_name, cv.stream_url, cv.value_
	FROM channel_values2 cv
	WHERE cv.channel_id NOT IN (SELECT f.channel_id FROM favourites f WHERE f.person_id = user_id)
    	ORDER BY value_ desc
    	LIMIT 3;
    	

END;
