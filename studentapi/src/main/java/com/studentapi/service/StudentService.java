package com.studentapi.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.studentapi.entities.Student;
import com.studentapi.repository.StudentRepository;

@Component
public class StudentService {
    
    @Autowired
    private StudentRepository studentRepository;

    //get all Students
    public List<Student> getAll() {
        return studentRepository.findAll();
    }

    //save Student
    public Student savStudent(Student student) {
        Student st = studentRepository.save(student);
        return st;
    }

    //Get single student
    public Student getStudentById(int id) {
        Student st = null;
        try {
            return this.studentRepository.findById(id);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return st;
    }

    //update student
    public boolean updateStudent(Student student, int id) {
        boolean f = false;
        try {
            student.setId(id);
            this.studentRepository.save(student);
            return f = true;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return f;
    }

    //Delete Student
    public boolean deleteStudent(int id) {
        boolean f = false;
        try {
            this.studentRepository.deleteById(id);
            return f = true;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return f;
    }


}
