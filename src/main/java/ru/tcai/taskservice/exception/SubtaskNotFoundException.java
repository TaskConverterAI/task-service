package ru.tcai.taskservice.exception;

public class SubtaskNotFoundException extends RuntimeException {
    public SubtaskNotFoundException(String message) {
        super(message);
    }
}
