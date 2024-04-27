-- SQL script that creates a stored procedure ComputeAverageScoreForUser
-- that computes and store the average score for a student. 
-- Note: An average score can be a decimal

DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(
    IN user_id INT
)
BEGIN
    DECLARE avg_score DECIMAL(10, 2);

    -- Compute the average score
    SELECT AVG(score) INTO avg_score
    FROM corrections
    WHERE corrections.user_id = user_id
    GROUP BY corrections.user_id;

    UPDATE users SET average_score = avg_score WHERE users.id = user_id;

END;
//

DELIMITER ;
