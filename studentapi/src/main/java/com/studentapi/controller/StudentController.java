package com.studentapi.controller;

import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import com.studentapi.entities.Student;
import com.studentapi.service.StudentService;

@RestController
public class StudentController {

    @Autowired
    private StudentService StudentService;
    
    //Get all Students
    @GetMapping("/students")
    public ResponseEntity<List<Student>> getAll() {
        try {
            List<Student> student = this.StudentService.getAll();
            if(student.size() <= 0) {
                return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
            } 
            return ResponseEntity.of(Optional.of(student));
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }   
    }

    //Create/Save students
    @PostMapping("/student")
    public ResponseEntity<Student> createStudent(@RequestBody Student st) {
        try {
            Student student = this.StudentService.savStudent(st);
            return ResponseEntity.of(Optional.of(student));
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }

    //Get single Student by Id
    @GetMapping("/student/{id}")
    public ResponseEntity<Student> getById(@PathVariable("id") int id) {
        Student student = this.StudentService.getStudentById(id);
        if(student == null) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        }
        return ResponseEntity.of(Optional.of(student));
    }

    //Update Studenet 
    @PutMapping("/student/{id}")
    public ResponseEntity<Student> updateStudent(@RequestBody Student student, @PathVariable("id") int id) {
        try {
            boolean f = StudentService.updateStudent(student, id);
            if(f == true) {
                return ResponseEntity.of(Optional.of(student));
            }
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }

    @DeleteMapping("/student/{id}")
    public ResponseEntity<Void> deleteStudent(@PathVariable("id") int id) {
        try {
            boolean f = StudentService.deleteStudent(id);
            if(f == true) {
                return ResponseEntity.ok().build();
            }
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }


}
