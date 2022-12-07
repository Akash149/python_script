package com.studentapi.repository;

import com.studentapi.entities.Student;

import java.util.List;

import org.springframework.data.repository.CrudRepository;

public interface StudentRepository extends CrudRepository<Student,Integer> {
    
    public Student findById(int id);
    public List<Student> findAll();

}
