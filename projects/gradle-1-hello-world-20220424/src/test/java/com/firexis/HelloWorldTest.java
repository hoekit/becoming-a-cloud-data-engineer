package com.firexis;

import org.junit.Test;

public class HelloWorldTest {

    @Test
    public void verifyNoExceptionThrown() {
        HelloWorld.main(new String[]{});
    }
}

/*
 * Add dependencies to build.gradle

dependencies {
    testImplementation group: 'junit', name: 'unit', version: '4.13.2'
}

 */
