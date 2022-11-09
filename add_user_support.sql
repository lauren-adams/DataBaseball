/* file: add_user_support.sql
 * description:
 *   Adds user support to the wii_baseball database by creating a 'user' table
 *   with a username and password. 
 *   
 *   The username is assumed to be less than or equal to 16 chars in length.
 *   
 *   The password will be encrypted with the SHA-1 algorithm. The SHA-1
 *   algorithm will transform the password into a 40-character string to be
 *   stored in the db.
 */
USE wii_baseball;
CREATE TABLE IF NOT EXISTS user (
    username VARCHAR(16) PRIMARY KEY,
    password VARCHAR(40) NOT NULL
);
