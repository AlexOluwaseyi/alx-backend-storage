-- SQL script that creates a stored procedure
-- ComputeAverageWeightedScoreForUser that computes
-- and store the average weighted score for a student.

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
    IN user_id INT
)
BEGIN
    DECLARE weighted_sum FLOAT;
    DECLARE total_weight INT;

    -- Initialize variables
    SET weighted_sum = 0;
    SET total_weight = 0;

    -- Calculate the weighted sum
    SELECT SUM(p.weight * c.score)
    INTO weighted_sum
    FROM corrections c
    INNER JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id;

    -- Calculate the total weight
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
END //

DELIMITER ;
