package com.studentapi.entities;

import com.fasterxml.jackson.annotation.JsonBackReference;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToOne;

@Entity
public class Address {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private int id;
    private String streetName;
    private String cityName;
    private String locality;
    private String stateName;
    private String countryName;
    @OneToOne(mappedBy = "address")
    @JsonBackReference //avoid the backloop
    private Student student;

    public Address() {
    }

    public int getId() {
        return id;
    }
    public void setId(int id) {
        this.id = id;
    }
    public String getStreetName() {
        return streetName;
    }
    public void setStreetName(String streetName) {
        this.streetName = streetName;
    }
    public String getCityName() {
        return cityName;
    }
    public void setCityName(String cityName) {
        this.cityName = cityName;
    }
    public String getLocality() {
        return locality;
    }
    public void setLocality(String locality) {
        this.locality = locality;
    }
    public String getStateName() {
        return stateName;
    }
    public void setStateName(String stateName) {
        this.stateName = stateName;
    }
    public String getCountryName() {
        return countryName;
    }
    public void setCountryName(String countryName) {
        this.countryName = countryName;
    }
    public Student getStudent() {
        return student;
    }
    public void setStudent(Student student) {
        this.student = student;
    }

    @Override
    public String toString() {
        return "Address [id=" + id + ", streetName=" + streetName + ", cityName=" + cityName + ", locality=" + locality
                + ", stateName=" + stateName + ", countryName=" + countryName + ", student=" + student + "]";
    }

    
}
