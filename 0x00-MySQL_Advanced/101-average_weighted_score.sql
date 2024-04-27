-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers
-- that computes and store the average weighted score for all students.

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE user_id INT;
    DECLARE weighted_sum FLOAT;
    DECLARE total_weight INT;

    -- Cursor to iterate over all users
    DECLARE user_cursor CURSOR FOR
        SELECT id FROM users;

    -- Declare exit handler for the cursor
    DECLARE CONTINUE HANDLER FOR NOT FOUND
        SET user_id = NULL;

    -- Open the cursor
    OPEN user_cursor;

    -- Loop through each user
    user_loop: LOOP
        -- Fetch the next user id
        FETCH user_cursor INTO user_id;

        -- Exit the loop if no more users
        IF user_id IS NULL THEN
            LEAVE user_loop;
        END IF;

        -- Reset variables for each user
        SET weighted_sum = 0;
        SET total_weight = 0;

        -- Calculate the weighted sum for the current user
        SELECT SUM(p.weight * c.score)
        INTO weighted_sum
        FROM corrections c
        INNER JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = user_id;

        -- Calculate the total weight of all projects
        SELECT SUM(weight)
        INTO total_weight
        FROM projects;

        -- Update the user's average score
        IF total_weight > 0 THEN
            UPDATE users
            SET average_score = weighted_sum / total_weight
            WHERE id = user_id;
        ELSE
            UPDATE users
            SET average_score = 0
            WHERE id = user_id;
        END IF;
    END LOOP;

    -- Close the cursor
    CLOSE user_cursor;
END //

DELIMITER ;

