/*
 * Copyright 2018-present Open Networking Foundation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.

 * This work was partially supported by EC H2020 project METRO-HAUL (761727).
 */

package org.onosproject.drivers.odtn;

import com.google.common.collect.ImmutableSet;
import org.onlab.util.Frequency;
import org.onlab.util.Spectrum;
import org.onosproject.net.ChannelSpacing;
import org.onosproject.net.GridType;
import org.onosproject.net.OchSignal;
import org.onosproject.net.PortNumber;
import org.onosproject.net.behaviour.LambdaQuery;
import org.onosproject.net.driver.AbstractHandlerBehaviour;

import java.util.Set;
import java.util.stream.IntStream;


public class GrooveOpenConfigLambdaQuery extends AbstractHandlerBehaviour implements LambdaQuery {
    private static final int LAMBDA_COUNT = 96;
    private static final Frequency START_CENTER_FREQ = Frequency.ofGHz(191_350);

    @Override
    public Set<OchSignal> queryLambdas(PortNumber port) {

        int startMultiplier = (int) (START_CENTER_FREQ.subtract(Spectrum.CENTER_FREQUENCY).asHz()
                / Frequency.ofGHz(50).asHz());

        return IntStream.range(0, LAMBDA_COUNT)
                .mapToObj(x -> new OchSignal(GridType.DWDM,
                                             ChannelSpacing.CHL_50GHZ,
                                             startMultiplier + x,
                                             4))
                .collect(ImmutableSet.toImmutableSet());
    }

}
