/*
 * Licensed to the Apache Software Foundation (ASF) under one   *
 * or more contributor license agreements.  See the NOTICE file *
 * distributed with this work for additional information        *
 * regarding copyright ownership.  The ASF licenses this file   *
 * to you under the Apache License, Version 2.0 (the            *
 * "License"); you may not use this file except in compliance   *
 * with the License.  You may obtain a copy of the License at   *
 *                                                              *
 *   http://www.apache.org/licenses/LICENSE-2.0                 *
 *                                                              *
 * Unless required by applicable law or agreed to in writing,   *
 * software distributed under the License is distributed on an  *
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY       *
 * KIND, either express or implied.  See the License for the    *
 * specific language governing permissions and limitations      *
 * under the License.                                           *
 */ 
package org.apache.rat.document;

import junit.framework.TestCase;

public class ToNameTransformerTest extends TestCase {

    ToNameTransformer transformer = new ToNameTransformer();
    
    protected void setUp() throws Exception {
        super.setUp();
    }

    protected void tearDown() throws Exception {
        super.tearDown();
    }

    public void testTransformLocation() {
        MockLocation location = new MockLocation();
        Object result = transformer.transform(location);
        assertNotNull("Transform into name", result);
        assertEquals("Transform into name", location.name, result);
    }

    public void testTransformNull() {
        Object result = transformer.transform(null);
        assertNull("Null transforms to null", result);
    }
}
